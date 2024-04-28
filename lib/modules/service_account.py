import copy
import datetime
import http.client as http_client
import json
import urllib

from lib.google.auth import _helpers
from lib.google.auth import _service_account_info
from lib.google.auth import credentials
from lib.google.auth import exceptions
from lib.google.auth import iam
from lib.google.auth import jwt
from lib.google.auth import metrics
from lib.google.auth import _exponential_backoff
from lib.google.auth import transport

_DEFAULT_TOKEN_LIFETIME_SECS = 3600  # 1 hour in seconds
_GOOGLE_OAUTH2_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
_URLENCODED_CONTENT_TYPE = "application/x-www-form-urlencoded"
_JSON_CONTENT_TYPE = "application/json"
_JWT_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"
_REFRESH_GRANT_TYPE = "refresh_token"

def _handle_error_response(response_data, retryable_error):
    """Translates an error response into an exception.

    Args:
        response_data (Mapping | str): The decoded response data.
        retryable_error Optional[bool]: A boolean indicating if an error is retryable.
            Defaults to False.

    Raises:
        google.auth.exceptions.RefreshError: The errors contained in response_data.
    """

    retryable_error = retryable_error if retryable_error else False

    if isinstance(response_data, str):
        raise exceptions.RefreshError(response_data, retryable=retryable_error)
    try:
        error_details = "{}: {}".format(
            response_data["error"], response_data.get("error_description")
        )
    # If no details could be extracted, use the response data.
    except (KeyError, ValueError):
        error_details = json.dumps(response_data)

    raise exceptions.RefreshError(
        error_details, response_data, retryable=retryable_error
    )


def _can_retry(status_code, response_data):
    """Checks if a request can be retried by inspecting the status code
    and response body of the request.

    Args:
        status_code (int): The response status code.
        response_data (Mapping | str): The decoded response data.

    Returns:
      bool: True if the response is retryable. False otherwise.
    """
    if status_code in transport.DEFAULT_RETRYABLE_STATUS_CODES:
        return True

    try:
        # For a failed response, response_body could be a string
        error_desc = response_data.get("error_description") or ""
        error_code = response_data.get("error") or ""

        if not isinstance(error_code, str) or not isinstance(error_desc, str):
            return False

        # Per Oauth 2.0 RFC https://www.rfc-editor.org/rfc/rfc6749.html#section-4.1.2.1
        # This is needed because a redirect will not return a 500 status code.
        retryable_error_descriptions = {
            "internal_failure",
            "server_error",
            "temporarily_unavailable",
        }

        if any(e in retryable_error_descriptions for e in (error_code, error_desc)):
            return True

    except AttributeError:
        pass

    return False


def _parse_expiry(response_data):
    """Parses the expiry field from a response into a datetime.

    Args:
        response_data (Mapping): The JSON-parsed response data.

    Returns:
        Optional[datetime]: The expiration or ``None`` if no expiration was
            specified.
    """
    expires_in = response_data.get("expires_in", None)

    if expires_in is not None:
        # Some services do not respect the OAUTH2.0 RFC and send expires_in as a
        # JSON String.
        if isinstance(expires_in, str):
            expires_in = int(expires_in)

        return _helpers.utcnow() + datetime.timedelta(seconds=expires_in)
    else:
        return None


def _token_endpoint_request_no_throw(
    request,
    token_uri,
    body,
    access_token=None,
    use_json=False,
    can_retry=True,
    headers=None,
    **kwargs
):

    if use_json:
        headers_to_use = {"Content-Type": _JSON_CONTENT_TYPE}
        body = json.dumps(body).encode("utf-8")
    else:
        headers_to_use = {"Content-Type": _URLENCODED_CONTENT_TYPE}
        body = urllib.parse.urlencode(body).encode("utf-8")

    if access_token:
        headers_to_use["Authorization"] = "Bearer {}".format(access_token)

    if headers:
        headers_to_use.update(headers)

    def _perform_request():
        response = request(
            method="POST", url=token_uri, headers=headers_to_use, body=body, **kwargs
        )
        response_body = (
            response.data.decode("utf-8")
            if hasattr(response.data, "decode")
            else response.data
        )
        response_data = ""
        try:
            # response_body should be a JSON
            response_data = json.loads(response_body)
        except ValueError:
            response_data = response_body

        if response.status == http_client.OK:
            return True, response_data, None

        retryable_error = _can_retry(
            status_code=response.status, response_data=response_data
        )

        return False, response_data, retryable_error

    request_succeeded, response_data, retryable_error = _perform_request()

    if request_succeeded or not retryable_error or not can_retry:
        return request_succeeded, response_data, retryable_error

    retries = _exponential_backoff.ExponentialBackoff()
    for _ in retries:
        request_succeeded, response_data, retryable_error = _perform_request()
        if request_succeeded or not retryable_error:
            return request_succeeded, response_data, retryable_error

    return False, response_data, retryable_error


def _token_endpoint_request(
    request,
    token_uri,
    body,
    access_token=None,
    use_json=False,
    can_retry=True,
    headers=None,
    **kwargs
):

    response_status_ok, response_data, retryable_error = _token_endpoint_request_no_throw(
        request,
        token_uri,
        body,
        access_token=access_token,
        use_json=use_json,
        can_retry=can_retry,
        headers=headers,
        **kwargs
    )
    if not response_status_ok:
        _handle_error_response(response_data, retryable_error)
    return response_data


def jwt_grant(request, token_uri, assertion, can_retry=True):
    
    body = {"assertion": assertion, "grant_type": _JWT_GRANT_TYPE}

    response_data = _token_endpoint_request(
        request,
        token_uri,
        body,
        can_retry=can_retry,
        headers={
            metrics.API_CLIENT_HEADER: metrics.token_request_access_token_sa_assertion()
        },
    )

    try:
        access_token = response_data["access_token"]
    except KeyError as caught_exc:
        new_exc = exceptions.RefreshError(
            "No access token in response.", response_data, retryable=False
        )
        raise new_exc from caught_exc

    expiry = _parse_expiry(response_data)

    return access_token, expiry, response_data


def call_iam_generate_id_token_endpoint(
    request, iam_id_token_endpoint, signer_email, audience, access_token
):
    body = {"audience": audience, "includeEmail": "true", "useEmailAzp": "true"}

    response_data = _token_endpoint_request(
        request,
        iam_id_token_endpoint.format(signer_email),
        body,
        access_token=access_token,
        use_json=True,
    )

    try:
        id_token = response_data["token"]
    except KeyError as caught_exc:
        new_exc = exceptions.RefreshError(
            "No ID token in response.", response_data, retryable=False
        )
        raise new_exc from caught_exc

    payload = jwt.decode(id_token, verify=False)
    expiry = datetime.datetime.utcfromtimestamp(payload["exp"])

    return id_token, expiry


def id_token_jwt_grant(request, token_uri, assertion, can_retry=True):
    body = {"assertion": assertion, "grant_type": _JWT_GRANT_TYPE}

    response_data = _token_endpoint_request(
        request,
        token_uri,
        body,
        can_retry=can_retry,
        headers={
            metrics.API_CLIENT_HEADER: metrics.token_request_id_token_sa_assertion()
        },
    )

    try:
        id_token = response_data["id_token"]
    except KeyError as caught_exc:
        new_exc = exceptions.RefreshError(
            "No ID token in response.", response_data, retryable=False
        )
        raise new_exc from caught_exc

    payload = jwt.decode(id_token, verify=False)
    expiry = datetime.datetime.utcfromtimestamp(payload["exp"])

    return id_token, expiry, response_data


def _handle_refresh_grant_response(response_data, refresh_token):
    try:
        access_token = response_data["access_token"]
    except KeyError as caught_exc:
        new_exc = exceptions.RefreshError(
            "No access token in response.", response_data, retryable=False
        )
        raise new_exc from caught_exc

    refresh_token = response_data.get("refresh_token", refresh_token)
    expiry = _parse_expiry(response_data)

    return access_token, refresh_token, expiry, response_data


def refresh_grant(
    request,
    token_uri,
    refresh_token,
    client_id,
    client_secret,
    scopes=None,
    rapt_token=None,
    can_retry=True,
):
    body = {
        "grant_type": _REFRESH_GRANT_TYPE,
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }
    if scopes:
        body["scope"] = " ".join(scopes)
    if rapt_token:
        body["rapt"] = rapt_token

    response_data = _token_endpoint_request(
        request, token_uri, body, can_retry=can_retry
    )
    return _handle_refresh_grant_response(response_data, refresh_token)


class Credentials(
    credentials.Signing,
    credentials.Scoped,
    credentials.CredentialsWithQuotaProject,
    credentials.CredentialsWithTokenUri,
):


    def __init__(
        self,
        signer,
        service_account_email,
        token_uri,
        scopes=None,
        default_scopes=None,
        subject=None,
        project_id=None,
        quota_project_id=None,
        additional_claims=None,
        always_use_jwt_access=False,
        universe_domain=credentials.DEFAULT_UNIVERSE_DOMAIN,
        trust_boundary=None,
    ):
        super(Credentials, self).__init__()

        self._scopes = scopes
        self._default_scopes = default_scopes
        self._signer = signer
        self._service_account_email = service_account_email
        self._subject = subject
        self._project_id = project_id
        self._quota_project_id = quota_project_id
        self._token_uri = token_uri
        self._always_use_jwt_access = always_use_jwt_access
        self._universe_domain = universe_domain or credentials.DEFAULT_UNIVERSE_DOMAIN

        if universe_domain != credentials.DEFAULT_UNIVERSE_DOMAIN:
            self._always_use_jwt_access = True

        self._jwt_credentials = None

        if additional_claims is not None:
            self._additional_claims = additional_claims
        else:
            self._additional_claims = {}
        self._trust_boundary = {"locations": [], "encoded_locations": "0x0"}

    @classmethod
    def _from_signer_and_info(cls, signer, info, **kwargs):
        """Creates a Credentials instance from a signer and service account
        info.

        Args:
            signer (google.auth.crypt.Signer): The signer used to sign JWTs.
            info (Mapping[str, str]): The service account info.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.jwt.Credentials: The constructed credentials.

        Raises:
            ValueError: If the info is not in the expected format.
        """
        return cls(
            signer,
            service_account_email=info["client_email"],
            token_uri=info["token_uri"],
            project_id=info.get("project_id"),
            universe_domain=info.get(
                "universe_domain", credentials.DEFAULT_UNIVERSE_DOMAIN
            ),
            trust_boundary=info.get("trust_boundary"),
            **kwargs
        )

    @classmethod
    def from_service_account_info(cls, info, **kwargs):
        """Creates a Credentials instance from parsed service account info.

        Args:
            info (Mapping[str, str]): The service account info in Google
                format.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.service_account.Credentials: The constructed
                credentials.

        Raises:
            ValueError: If the info is not in the expected format.
        """
        signer = _service_account_info.from_dict(
            info, require=["client_email", "token_uri"]
        )
        return cls._from_signer_and_info(signer, info, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename, **kwargs):
        """Creates a Credentials instance from a service account json file.

        Args:
            filename (str): The path to the service account json file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.service_account.Credentials: The constructed
                credentials.
        """
        info, signer = _service_account_info.from_filename(
            filename, require=["client_email", "token_uri"]
        )
        return cls._from_signer_and_info(signer, info, **kwargs)

    @property
    def service_account_email(self):
        """The service account email."""
        return self._service_account_email

    @property
    def project_id(self):
        """Project ID associated with this credential."""
        return self._project_id

    @property
    def requires_scopes(self):
        """Checks if the credentials requires scopes.

        Returns:
            bool: True if there are no scopes set otherwise False.
        """
        return True if not self._scopes else False

    def _make_copy(self):
        cred = self.__class__(
            self._signer,
            service_account_email=self._service_account_email,
            scopes=copy.copy(self._scopes),
            default_scopes=copy.copy(self._default_scopes),
            token_uri=self._token_uri,
            subject=self._subject,
            project_id=self._project_id,
            quota_project_id=self._quota_project_id,
            additional_claims=self._additional_claims.copy(),
            always_use_jwt_access=self._always_use_jwt_access,
            universe_domain=self._universe_domain,
        )
        return cred

    @_helpers.copy_docstring(credentials.Scoped)
    def with_scopes(self, scopes, default_scopes=None):
        cred = self._make_copy()
        cred._scopes = scopes
        cred._default_scopes = default_scopes
        return cred

    def with_always_use_jwt_access(self, always_use_jwt_access):
        """Create a copy of these credentials with the specified always_use_jwt_access value.

        Args:
            always_use_jwt_access (bool): Whether always use self signed JWT or not.

        Returns:
            google.auth.service_account.Credentials: A new credentials
                instance.
        Raises:
            google.auth.exceptions.InvalidValue: If the universe domain is not
                default and always_use_jwt_access is False.
        """
        cred = self._make_copy()
        if (
            cred._universe_domain != credentials.DEFAULT_UNIVERSE_DOMAIN
            and not always_use_jwt_access
        ):
            raise exceptions.InvalidValue(
                "always_use_jwt_access should be True for non-default universe domain"
            )
        cred._always_use_jwt_access = always_use_jwt_access
        return cred

    @_helpers.copy_docstring(credentials.CredentialsWithUniverseDomain)
    def with_universe_domain(self, universe_domain):
        cred = self._make_copy()
        cred._universe_domain = universe_domain
        if universe_domain != credentials.DEFAULT_UNIVERSE_DOMAIN:
            cred._always_use_jwt_access = True
        return cred

    def with_subject(self, subject):
        """Create a copy of these credentials with the specified subject.

        Args:
            subject (str): The subject claim.

        Returns:
            google.auth.service_account.Credentials: A new credentials
                instance.
        """
        cred = self._make_copy()
        cred._subject = subject
        return cred

    def with_claims(self, additional_claims):
        """Returns a copy of these credentials with modified claims.

        Args:
            additional_claims (Mapping[str, str]): Any additional claims for
                the JWT payload. This will be merged with the current
                additional claims.

        Returns:
            google.auth.service_account.Credentials: A new credentials
                instance.
        """
        new_additional_claims = copy.deepcopy(self._additional_claims)
        new_additional_claims.update(additional_claims or {})
        cred = self._make_copy()
        cred._additional_claims = new_additional_claims
        return cred

    @_helpers.copy_docstring(credentials.CredentialsWithQuotaProject)
    def with_quota_project(self, quota_project_id):
        cred = self._make_copy()
        cred._quota_project_id = quota_project_id
        return cred

    @_helpers.copy_docstring(credentials.CredentialsWithTokenUri)
    def with_token_uri(self, token_uri):
        cred = self._make_copy()
        cred._token_uri = token_uri
        return cred

    def _make_authorization_grant_assertion(self):
        """Create the OAuth 2.0 assertion.

        This assertion is used during the OAuth 2.0 grant to acquire an
        access token.

        Returns:
            bytes: The authorization grant assertion.
        """
        now = _helpers.utcnow()
        lifetime = datetime.timedelta(seconds=_DEFAULT_TOKEN_LIFETIME_SECS)
        expiry = now + lifetime

        payload = {
            "iat": _helpers.datetime_to_secs(now),
            "exp": _helpers.datetime_to_secs(expiry),
            # The issuer must be the service account email.
            "iss": self._service_account_email,
            # The audience must be the auth token endpoint's URI
            "aud": _GOOGLE_OAUTH2_TOKEN_ENDPOINT,
            "scope": _helpers.scopes_to_string(self._scopes or ()),
        }

        payload.update(self._additional_claims)

        # The subject can be a user email for domain-wide delegation.
        if self._subject:
            payload.setdefault("sub", self._subject)

        token = jwt.encode(self._signer, payload)

        return token

    def _use_self_signed_jwt(self):
        # Since domain wide delegation doesn't work with self signed JWT. If
        # subject exists, then we should not use self signed JWT.
        return self._subject is None and self._jwt_credentials is not None

    def _metric_header_for_usage(self):
        if self._use_self_signed_jwt():
            return metrics.CRED_TYPE_SA_JWT
        return metrics.CRED_TYPE_SA_ASSERTION

    @_helpers.copy_docstring(credentials.Credentials)
    def refresh(self, request):
        if self._always_use_jwt_access and not self._jwt_credentials:
            # If self signed jwt should be used but jwt credential is not
            # created, try to create one with scopes
            self._create_self_signed_jwt(None)

        if (
            self._universe_domain != credentials.DEFAULT_UNIVERSE_DOMAIN
            and self._subject
        ):
            raise exceptions.RefreshError(
                "domain wide delegation is not supported for non-default universe domain"
            )

        if self._use_self_signed_jwt():
            self._jwt_credentials.refresh(request)
            self.token = self._jwt_credentials.token.decode()
            self.expiry = self._jwt_credentials.expiry
        else:
            assertion = self._make_authorization_grant_assertion()
            access_token, expiry, _ = jwt_grant(
                request, self._token_uri, assertion
            )
            self.token = access_token
            self.expiry = expiry

    def _create_self_signed_jwt(self, audience):
        """Create a self-signed JWT from the credentials if requirements are met.

        Args:
            audience (str): The service URL. ``https://[API_ENDPOINT]/``
        """
        # https://google.aip.dev/auth/4111
        if self._always_use_jwt_access:
            if self._scopes:
                additional_claims = {"scope": " ".join(self._scopes)}
                if (
                    self._jwt_credentials is None
                    or self._jwt_credentials.additional_claims != additional_claims
                ):
                    self._jwt_credentials = jwt.Credentials.from_signing_credentials(
                        self, None, additional_claims=additional_claims
                    )
            elif audience:
                if (
                    self._jwt_credentials is None
                    or self._jwt_credentials._audience != audience
                ):

                    self._jwt_credentials = jwt.Credentials.from_signing_credentials(
                        self, audience
                    )
            elif self._default_scopes:
                additional_claims = {"scope": " ".join(self._default_scopes)}
                if (
                    self._jwt_credentials is None
                    or additional_claims != self._jwt_credentials.additional_claims
                ):
                    self._jwt_credentials = jwt.Credentials.from_signing_credentials(
                        self, None, additional_claims=additional_claims
                    )
        elif not self._scopes and audience:
            self._jwt_credentials = jwt.Credentials.from_signing_credentials(
                self, audience
            )

    @_helpers.copy_docstring(credentials.Signing)
    def sign_bytes(self, message):
        return self._signer.sign(message)

    @property  # type: ignore
    @_helpers.copy_docstring(credentials.Signing)
    def signer(self):
        return self._signer

    @property  # type: ignore
    @_helpers.copy_docstring(credentials.Signing)
    def signer_email(self):
        return self._service_account_email


class IDTokenCredentials(
    credentials.Signing,
    credentials.CredentialsWithQuotaProject,
    credentials.CredentialsWithTokenUri,
):
    """Open ID Connect ID Token-based service account credentials.

    These credentials are largely similar to :class:`.Credentials`, but instead
    of using an OAuth 2.0 Access Token as the bearer token, they use an Open
    ID Connect ID Token as the bearer token. These credentials are useful when
    communicating to services that require ID Tokens and can not accept access
    tokens.

    Usually, you'll create these credentials with one of the helper
    constructors. To create credentials using a Google service account
    private key JSON file::

        credentials = (
            service_account.IDTokenCredentials.from_service_account_file(
                'service-account.json'))


    Or if you already have the service account file loaded::

        service_account_info = json.load(open('service_account.json'))
        credentials = (
            service_account.IDTokenCredentials.from_service_account_info(
                service_account_info))


    Both helper methods pass on arguments to the constructor, so you can
    specify additional scopes and a subject if necessary::

        credentials = (
            service_account.IDTokenCredentials.from_service_account_file(
                'service-account.json',
                scopes=['email'],
                subject='user@example.com'))


    The credentials are considered immutable. If you want to modify the scopes
    or the subject used for delegation, use :meth:`with_scopes` or
    :meth:`with_subject`::

        scoped_credentials = credentials.with_scopes(['email'])
        delegated_credentials = credentials.with_subject(subject)

    """

    def __init__(
        self,
        signer,
        service_account_email,
        token_uri,
        target_audience,
        additional_claims=None,
        quota_project_id=None,
        universe_domain=credentials.DEFAULT_UNIVERSE_DOMAIN,
    ):
        """
        Args:
            signer (google.auth.crypt.Signer): The signer used to sign JWTs.
            service_account_email (str): The service account's email.
            token_uri (str): The OAuth 2.0 Token URI.
            target_audience (str): The intended audience for these credentials,
                used when requesting the ID Token. The ID Token's ``aud`` claim
                will be set to this string.
            additional_claims (Mapping[str, str]): Any additional claims for
                the JWT assertion used in the authorization grant.
            quota_project_id (Optional[str]): The project ID used for quota and billing.
            universe_domain (str): The universe domain. The default
                universe domain is googleapis.com. For default value IAM ID
                token endponint is used for token refresh. Note that
                iam.serviceAccountTokenCreator role is required to use the IAM
                endpoint.
        .. note:: Typically one of the helper constructors
            :meth:`from_service_account_file` or
            :meth:`from_service_account_info` are used instead of calling the
            constructor directly.
        """
        super(IDTokenCredentials, self).__init__()
        self._signer = signer
        self._service_account_email = service_account_email
        self._token_uri = token_uri
        self._target_audience = target_audience
        self._quota_project_id = quota_project_id
        self._use_iam_endpoint = False

        if not universe_domain:
            self._universe_domain = credentials.DEFAULT_UNIVERSE_DOMAIN
        else:
            self._universe_domain = universe_domain
        self._iam_id_token_endpoint = iam._IAM_IDTOKEN_ENDPOINT.replace(
            "googleapis.com", self._universe_domain
        )

        if self._universe_domain != credentials.DEFAULT_UNIVERSE_DOMAIN:
            self._use_iam_endpoint = True

        if additional_claims is not None:
            self._additional_claims = additional_claims
        else:
            self._additional_claims = {}

    @classmethod
    def _from_signer_and_info(cls, signer, info, **kwargs):
        """Creates a credentials instance from a signer and service account
        info.

        Args:
            signer (google.auth.crypt.Signer): The signer used to sign JWTs.
            info (Mapping[str, str]): The service account info.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.jwt.IDTokenCredentials: The constructed credentials.

        Raises:
            ValueError: If the info is not in the expected format.
        """
        kwargs.setdefault("service_account_email", info["client_email"])
        kwargs.setdefault("token_uri", info["token_uri"])
        if "universe_domain" in info:
            kwargs["universe_domain"] = info["universe_domain"]
        return cls(signer, **kwargs)

    @classmethod
    def from_service_account_info(cls, info, **kwargs):
        """Creates a credentials instance from parsed service account info.

        Args:
            info (Mapping[str, str]): The service account info in Google
                format.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.service_account.IDTokenCredentials: The constructed
                credentials.

        Raises:
            ValueError: If the info is not in the expected format.
        """
        signer = _service_account_info.from_dict(
            info, require=["client_email", "token_uri"]
        )
        return cls._from_signer_and_info(signer, info, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename, **kwargs):
        """Creates a credentials instance from a service account json file.

        Args:
            filename (str): The path to the service account json file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.service_account.IDTokenCredentials: The constructed
                credentials.
        """
        info, signer = _service_account_info.from_filename(
            filename, require=["client_email", "token_uri"]
        )
        return cls._from_signer_and_info(signer, info, **kwargs)

    def _make_copy(self):
        cred = self.__class__(
            self._signer,
            service_account_email=self._service_account_email,
            token_uri=self._token_uri,
            target_audience=self._target_audience,
            additional_claims=self._additional_claims.copy(),
            quota_project_id=self.quota_project_id,
            universe_domain=self._universe_domain,
        )
        # _use_iam_endpoint is not exposed in the constructor
        cred._use_iam_endpoint = self._use_iam_endpoint
        return cred

    def with_target_audience(self, target_audience):
        """Create a copy of these credentials with the specified target
        audience.

        Args:
            target_audience (str): The intended audience for these credentials,
            used when requesting the ID Token.

        Returns:
            google.auth.service_account.IDTokenCredentials: A new credentials
                instance.
        """
        cred = self._make_copy()
        cred._target_audience = target_audience
        return cred

    def _with_use_iam_endpoint(self, use_iam_endpoint):
        """Create a copy of these credentials with the use_iam_endpoint value.

        Args:
            use_iam_endpoint (bool): If True, IAM generateIdToken endpoint will
                be used instead of the token_uri. Note that
                iam.serviceAccountTokenCreator role is required to use the IAM
                endpoint. The default value is False. This feature is currently
                experimental and subject to change without notice.

        Returns:
            google.auth.service_account.IDTokenCredentials: A new credentials
                instance.
        Raises:
            google.auth.exceptions.InvalidValue: If the universe domain is not
                default and use_iam_endpoint is False.
        """
        cred = self._make_copy()
        if (
            cred._universe_domain != credentials.DEFAULT_UNIVERSE_DOMAIN
            and not use_iam_endpoint
        ):
            raise exceptions.InvalidValue(
                "use_iam_endpoint should be True for non-default universe domain"
            )
        cred._use_iam_endpoint = use_iam_endpoint
        return cred

    @_helpers.copy_docstring(credentials.CredentialsWithQuotaProject)
    def with_quota_project(self, quota_project_id):
        cred = self._make_copy()
        cred._quota_project_id = quota_project_id
        return cred

    @_helpers.copy_docstring(credentials.CredentialsWithTokenUri)
    def with_token_uri(self, token_uri):
        cred = self._make_copy()
        cred._token_uri = token_uri
        return cred

    def _make_authorization_grant_assertion(self):
        """Create the OAuth 2.0 assertion.

        This assertion is used during the OAuth 2.0 grant to acquire an
        ID token.

        Returns:
            bytes: The authorization grant assertion.
        """
        now = _helpers.utcnow()
        lifetime = datetime.timedelta(seconds=_DEFAULT_TOKEN_LIFETIME_SECS)
        expiry = now + lifetime

        payload = {
            "iat": _helpers.datetime_to_secs(now),
            "exp": _helpers.datetime_to_secs(expiry),
            # The issuer must be the service account email.
            "iss": self.service_account_email,
            # The audience must be the auth token endpoint's URI
            "aud": _GOOGLE_OAUTH2_TOKEN_ENDPOINT,
            # The target audience specifies which service the ID token is
            # intended for.
            "target_audience": self._target_audience,
        }

        payload.update(self._additional_claims)

        token = jwt.encode(self._signer, payload)

        return token

    def _refresh_with_iam_endpoint(self, request):
        """Use IAM generateIdToken endpoint to obtain an ID token.

        It works as follows:

        1. First we create a self signed jwt with
        https://www.googleapis.com/auth/iam being the scope.

        2. Next we use the self signed jwt as the access token, and make a POST
        request to IAM generateIdToken endpoint. The request body is:
            {
                "audience": self._target_audience,
                "includeEmail": "true",
                "useEmailAzp": "true",
            }

        If the request is succesfully, it will return {"token":"the ID token"},
        and we can extract the ID token and compute its expiry.
        """
        jwt_credentials = jwt.Credentials.from_signing_credentials(
            self,
            None,
            additional_claims={"scope": "https://www.googleapis.com/auth/iam"},
        )
        jwt_credentials.refresh(request)
        self.token, self.expiry = call_iam_generate_id_token_endpoint(
            request,
            self._iam_id_token_endpoint,
            self.signer_email,
            self._target_audience,
            jwt_credentials.token.decode(),
        )

    @_helpers.copy_docstring(credentials.Credentials)
    def refresh(self, request):
        if self._use_iam_endpoint:
            self._refresh_with_iam_endpoint(request)
        else:
            assertion = self._make_authorization_grant_assertion()
            access_token, expiry, _ = id_token_jwt_grant(
                request, self._token_uri, assertion
            )
            self.token = access_token
            self.expiry = expiry

    @property
    def service_account_email(self):
        """The service account email."""
        return self._service_account_email

    @_helpers.copy_docstring(credentials.Signing)
    def sign_bytes(self, message):
        return self._signer.sign(message)

    @property  # type: ignore
    @_helpers.copy_docstring(credentials.Signing)
    def signer(self):
        return self._signer

    @property  # type: ignore
    @_helpers.copy_docstring(credentials.Signing)
    def signer_email(self):
        return self._service_account_email
