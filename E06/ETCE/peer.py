from nacl.public import PrivateKey, PublicKey
from nacl.signing import SigningKey, VerifyKey, SignedMessage
from nacl.encoding import RawEncoder
from nacl.utils import EncryptedMessage

class Ex06Solution(object):
    """
    Interface class for Ex05 Solution
    """
    def __init__(self):
        self.__peer_signingkey__ = SigningKey(b'\xc7\xc7\t\x12uI\x9b\x18q\xd3\xb7\xc6e\xea\xa4\xba0\xe0Lj\x03V/\xeek\x874#\x0e>\x06r',
                                              encoder=RawEncoder)

        self.__peer_ephermal_priv__ = PrivateKey(b'\x89\xf7,&\xd9\xc6\x81\xf6\x86!w9\xb9\xb3\x9c\x1f\xa9W\xcf\x9f\xb5\xd0\xe4\xa9\x86\xb6\x15XKd\xe8\x1d',
                                                   encoder=RawEncoder)

        self.__peer_signed_ephermal_pub__ = SignedMessage(b"#\x91+y#\xbaYS\xe0\x00\x9e\xb8\xc1md\xa0\xc1aLNPC\xf6a\xa63A\xddB\xef\x11x\xdd\x89\x85\x93\x93O\xa6\xa2\xbb\xa7\x8e9\xef^\xf7\x97\xd0@l\xd0\xb5\x8a\xc1\xb7o\xcb\x00\x02l\xe1\x9f\x01\xe6\x14\xe5\x00S$@=\xbc!\xc8k\x9b@\x9a[t\x0c\xc3M)\x94\xb0\x7f'+\x8c\xb7\r\xc0\xb7\x7f")
        self.__peer_signed_ephermal_pub__.__dict__ = {'_signature': b'#\x91+y#\xbaYS\xe0\x00\x9e\xb8\xc1md\xa0\xc1aLNPC\xf6a\xa63A\xddB\xef\x11x\xdd\x89\x85\x93\x93O\xa6\xa2\xbb\xa7\x8e9\xef^\xf7\x97\xd0@l\xd0\xb5\x8a\xc1\xb7o\xcb\x00\x02l\xe1\x9f\x01',
                                                       '_message': b"\xe6\x14\xe5\x00S$@=\xbc!\xc8k\x9b@\x9a[t\x0c\xc3M)\x94\xb0\x7f'+\x8c\xb7\r\xc0\xb7\x7f"}

        self.peer_verifykey = None

        self.derived_key = None

        self.dk_salt = b'\xf6o+\xabL\x98WM=S\xde\xe2\xe0\xe6\t\x85'

        self.encrypted_personal_signingkey = b'\xa5\xd5\r\x83\xc3m\xe1E:PV\xe1\x14@\n\xc4\x11\x17\xecZ\xe90X\xb9\xb3I\x87\xfe\xbf.D7\xb47S\xf8z\xf2}\xd2\xd7\xc0\xe8"\xff7\xa98\xf2z\xa8G\x12\x90\x9d\x02f\xe4\x85\xbd\x7f\x9f\xb7E\xf5\xc9Ql\x0e\xf6Ke' 

        self.personal_signingkey = None

        (self.personal_ephermal_pubkey, self.personal_ephermal_privkey) = (None, None)
        
        self.peer_ephermal_pubkey = None

        self.ECDH_box = None
        
        self.__buyers_intervals__ = [{"charging_start": 1618056000,
                                      "charging_end": 1618059600,
                                      "charging_duration": 3600,
                                      "charging_station_name": "Charging Station 1",
                                      "energy_provider_name": "Energy Provider 2",
                                      "battery_energy_before": 0,
                                      "battery_energy_after": 10,
                                      "energy_bought": 10,
                                      "price":None 
                                      },
                                     {"charging_start": 1618063200,
                                      "charging_end": 1618066800,
                                      "charging_duration": 3600,
                                      "charging_station_name": "Charging Station 1",
                                      "energy_provider_name": "Energy Provider 2",
                                      "battery_energy_before": 0,
                                      "battery_energy_after": 10,
                                      "energy_bought": 10,
                                      "price":None 
                                      },
                                     {"charging_start": 1618077600,
                                      "charging_end": 1618081200,
                                      "charging_duration": 3600,
                                      "charging_station_name": "Charging Station 1",
                                      "energy_provider_name": "Energy Provider 2",
                                      "battery_energy_before": 0,
                                      "battery_energy_after": 10,
                                      "energy_bought": 10,
                                      "price":None 
                                      }]
        self.__sellers_price__ = 20
    def get_peer_pubkey(self) -> bytes:
        """This function will give you the encoded public key
        (`nacl.signing.VerifyKey`) for your peer.

        Public key was encoded using the
        `nacl.signing.VerifyKey.encode()` method using
        `nacl.encoding.RawEncoder`

        https://pynacl.readthedocs.io/en/stable/

        DO NOT OVERRIDE THIS METHOD

        """
        return self.__peer_signingkey__.verify_key.encode(encoder=RawEncoder)

    def get_peer_ephermal_pubkey_signed(self) -> SignedMessage:
        """This function will return the signed ephermal public key for your
        peer.

        Assume that the public key is encoded using
        `nacl.encoding.RawEncoder`
        
        DO NOT OVERRIDE THIS METHOD

        """
        return self.__peer_signed_ephermal_pub__

    def get_buyer_options(self) -> list:
        """This function will return the list of charging interval options for
        a particular day for the Energy Buyers. Each option has the structure:
 
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
        The `price` value will be None
        
        DO NOT OVERRIDE THIS METHOD

        """
        return self.__buyers_intervals__

    def get_sellers_selling_rate(self) -> float:
        """This function will return the price(per kWh) in c€ for Energy
        Sellers.
        
        DO NOT OVERRIDE THIS METHOD

        """
        return self.__sellers_price__

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
        your handout tar.
        
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
        """
        This function should use the shared secret from
        `self.ECDH_box` to use as a key to create a
        `nacl.secret.SecretBox` object and then use this as an
        authenticated encryption mechanism to decrypt the
        `encrypted_message`, which is a `nacl.utils.EncryptedMessage`
        instance and return the plaintext bytes.

        """
        pass
    
    def encrypt(self, plaintext_bytes) -> EncryptedMessage:
        """
        This function should use the shared secret from
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
        that this is possible before you submit your handout tar.

        OVERRIDE THIS METHOD

        """
        pass
