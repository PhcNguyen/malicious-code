

from __future__ import annotations

import abc

# This exists to break an import cycle. It is normally accessible from the
# asymmetric padding module.


class AsymmetricPadding(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        A string naming this padding (e.g. "PSS", "PKCS1").
        """
