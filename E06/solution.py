import json
from nacl.utils import EncryptedMessage
from nacl.signing import SignedMessage
# You can import everything else you might need from nacl

from ETCE.peer import Ex06Solution

class Solution(Ex06Solution):
    """This class should implement the solution for Ex06
    
    Override the methods in this class by following the corresponding
    instructions given in the docstrings in `ETCE.peer.Ex06Solution`

    """
    def __init__(self):
        super(Solution, self).__init__()

    def derive_symm_key(self) -> None:
        """Step 1. of the Excercise Sheet
        
        This function should derive the symmetric key of size
        nacl.secret.SecretBox.KEY_SIZE using the argon2id key
        derivation function using the password and salt provided
        (self.dk_salt) and set the class variable `self.derived_key`
        by initializing a `nacl.secret.SecretBox` object. Use the
        `SENSITIVE` ops and mem limits.
        
        https://pynacl.readthedocs.io/en/stable/
        
        OVERRIDE THIS METHOD

        """
        pass

    def load_personal_privkey(self) -> bytes:
        """Step 2. of the Excercise Sheet
        
        https://pynacl.readthedocs.io/en/stable/

        This function should load your personal private key
        (`nacl.signing.SigningKey`) using the DerivedKey
        (`self.derived_key`) and Encrypted Private Key
        (`self.encrypted_personal_signingkey`) and set the class
        variable `self.personal_signingkey` by initializing a
        `nacl.signing.SigningKey` object
        
        Assume that the Encrypted Private Key provided to you is the
        result of encrypting the encoded bytes returned by the
        `nacl.signing.SigningKey.encode()` method using the
        `nacl.encoding.RawEncoder`. Encode and return the associated
        personal public key (`nacl.signing.VerifyKey`) using the same
        encoder.
        
        https://pynacl.readthedocs.io/en/stable/

        OVERRIDE THIS METHOD

        """
        pass

    def load_peer_pubkey(self) -> None:
        """Step 3. of the Excercise Sheet

        This function should load your peer's public key
        (`nacl.signing.VerifyKey`) using `self.get_peer_pubkey()` and
        set the class variable `self.peer_verifykey` by initializing a
        `nacl.signing.VerifyKey` object
        
        OVERRIDE THIS METHOD
        
        """
        pass

    def generate_ephermal_keypair(self) -> SignedMessage:
        """Step 4. of the Excercise Sheet

        This function should generate an ephermal keypair and set the
        class variables `self.personal_ephermal_pubkey` and
        `self.personal_ephermal_privkey`. Encode the ephermal public
        key using the `nacl.encoding.RawEncoder`.

        https://pynacl.readthedocs.io/en/stable/encoding/#nacl.encoding.RawEncoder

        Sign this encoded public key using your personal private key
        and return an instance of `nacl.signing.SignedMessage`
        
        The signed message will be verified by your peer

        So as to not give you the solution pertaining to the
        verification of a SignedMessage, the grading tool provided to
        you will not Actually verify the message, but only check if it
        is correctly instantiated. The evaluation `driver.py`, however
        WILL attempt to verify using your signed ephermal public key
        using your personal public key which was returned earlier in
        Step 2. So make sure that this is possible before you submit
        your handout zip.
        
        OVERRIDE THIS METHOD

        """
        pass

    def receive_ephermal_pubkey(self) -> bool:
        """Step 5. of the Excercise Sheet
        
        This function should receive the signed ephermal public key
        for the peer by calling
        `self.get_peer_ephermal_pubkey_signed()`

        Verify the signature, and set the class variable
        `self.peer_ephermal_pubkey` as an instance of
        `nacl.public.PublicKey` ONLY IF the verification is
        successful.

        Also, return the boolean result of the verification

        OVERRIDE THIS METHOD
        """
        pass
    
    def perform_ecdh_keyexchange(self) -> None:
        """Step 6. of the Excercise Sheet

        This function should use your ephermal private key and your
        peer's ephermal public key to perform an ECDH key exchange, by
        setting the class variable `self.ECDH_box` as an instance of
        `nacl.public.Box`

        OVERRIDE THIS METHOD
        """
        pass

    def decrypt(self, encrypted_message) -> bytes:
        """This function should use the shared secret from
        `self.ECDH_box` to use as a key to create a
        `nacl.secret.SecretBox` object and then use this as an
        authenticated encryption mechanism to decrypt the
        `encrypted_message`, which is a `nacl.utils.EncryptedMessage`
        instance and return the plaintext bytes.

        """
        pass
    
    def encrypt(self, plaintext_bytes) -> EncryptedMessage:
        """This function should use the shared secret from
        `self.ECDH_box` to use as a key to create a
        `nacl.secret.SecretBox` object and then use this as an
        authenticated encryption mechanism to encrypt the
        `plaintext_bytes`, which is a `bytes` instance and return a
        `nacl.utils.EncryptedMessage` instance.

        """
        pass
    
    def seller_decrypt_purchase_request(self, encrypted_purchase_request) -> EncryptedMessage:
        """Step 7. of the Excercise Sheet

        This function should use the shared secret from
        `self.ECDH_box` to use as a key to create a
        `nacl.secret.SecretBox` object and then use this as an
        authenticated encryption mechanism to decrypt the
        `encrypted_purchase_request`. Use utf-8 decoding to produce
        the plaintext json string. Decode the json string into a
        python dictionary.

        Expect a dictionary structure of the following format:

        {"charging_start": <integer timestamp>,
        "charging_end": <integer timestamp>,
        "charging_duration": <integer> seconds,
        "charging_station_name": <string >,
        "energy_provider_name": <string >,
        "battery_energy_before": <float kWh>,
        "battery_energy_after": <float kWh>,
        "energy_bought": <float kWh>,
        "price": <float €>
        }

        Compute the price (in €) that you will charge the buyer, by
        using the `energy_bought` value of the purchase request and
        the price per kWh, which can be obtained by calling the
        function `self.get_sellers_selling_rate()` which returns c€.

        Round this price to the nearest 2 decimal places and convert
        it to string. Using utf-8 encoding generate the plaintext
        bytes, encrypt it using the previously created SecretBox and
        return an `nacl.utils.EncryptedMessage` object.

        IMPORTANT: Generate a new nonce.

        The encrypted price will be decrypted by your peer.

        So as to not give you the solution pertaining to the
        decryption of an EncryptedMessage, the grading tool provided
        to you will not Actually decrypt the message, but only check
        if it is correctly instantiated. The evaluation `driver.py`,
        however WILL attempt to decrypt using your signed ephermal
        public key and the peer's ephermal private key. So make sure
        that this is possible before you submit your handout zip.

        OVERRIDE THIS METHOD

        """
        pass
