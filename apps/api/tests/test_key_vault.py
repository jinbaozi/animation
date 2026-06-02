import pytest

from app.services.key_vault import EncryptedSecret, decrypt_secret, encrypt_secret


def test_encrypt_secret_round_trips_with_master_password():
    encrypted = encrypt_secret("master-pass", "sk-test-123")

    assert encrypted.ciphertext != "sk-test-123"
    assert decrypt_secret("master-pass", encrypted) == "sk-test-123"


def test_decrypt_secret_rejects_wrong_master_password():
    encrypted = encrypt_secret("master-pass", "sk-test-123")

    with pytest.raises(ValueError, match="Unable to decrypt API key"):
        decrypt_secret("wrong-pass", encrypted)


def test_decrypt_secret_rejects_malformed_base64_fields():
    encrypted = EncryptedSecret(
        salt="not-valid-base64===",
        nonce="not-valid-base64===",
        ciphertext="not-valid-base64===",
    )

    with pytest.raises(ValueError, match="Unable to decrypt API key"):
        decrypt_secret("master-pass", encrypted)
