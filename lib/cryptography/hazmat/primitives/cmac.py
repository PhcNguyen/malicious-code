

from __future__ import annotations

from cryptography.hazmat.bindings._rust import openssl as rust_openssl

__all__ = ["CMAC"]
CMAC = rust_openssl.cmac.CMAC
