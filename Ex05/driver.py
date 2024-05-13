try:
    from solution import Solution as Solution_A
except Exception as E:
    print(E)
    print("0,0")
from nacl.secret import SecretBox
from nacl.encoding import RawEncoder
from nacl.public import PublicKey, Box, EncryptedMessage
from nacl.signing import VerifyKey, SignedMessage
from nacl.hash import sha256
import json


def check_solution(solution_object):
    step1_pass = False
    try:
        solution_object.derive_symm_key()
        if sha256(
                solution_object.derived_key.encode()) == b'5040002df51098b4b94f4bad8dc0913d9dc5d790d8572bfbc9b0fc334c1b1262':
            step1_pass = True
    except Exception as E:
        print(E)
        step1_pass = False
    if not step1_pass:
        print(
            "Step 1 failed: Please check the derive_symm_key() function if you are setting the variable self.derived_key correctly.")

    step2_pass = False
    try:
        if sha256(
                solution_object.load_personal_privkey()) == b'cf5563f4b5c3db347d61a6b891b06e20ce030b4fe238ff8651dff57e877fbc1c':
            step2_pass = True
    except Exception as E:
        print(E)
        step2_pass = False

    if not step2_pass:
        print(
            "Step 2 failed: Please check the load_personal_privkey() function if you are setting (and returning) the variable self.personal_signingkey correctly.")

    step3_pass = False
    try:
        solution_object.load_peer_pubkey()
        if sha256(
                solution_object.peer_verifykey.encode()) == b'31bdcb13b1e1e2ccf3c34571fcde5f2e4c1c8f66ec15baee5eba6d1b44dc78f2':
            step3_pass = True
    except Exception as E:
        print(E)
        step3_pass = False

    if not step3_pass:
        print(
            "Step 3 failed: Please check the load_peer_pubkey() function if you are setting the variable self.peer_verifykey correctly.")

    step4_pass = False
    try:
        signed_message = solution_object.generate_ephermal_keypair()
        if isinstance(signed_message, SignedMessage):
            step4_pass = True
    except Exception as E:
        print(E)
        step4_pass = False

    if not step4_pass:
        print(
            "Step 4 failed: Please check the generate_ephermal_keypair() function if you are correctly instantiating a nacl.signing.SignedMessage object")

    step5_pass = False
    try:
        psep = solution_object.__peer_signed_ephermal_pub__
        forged_psep = solution_object.__peer_signed_ephermal_pub__[:-1] + bytes(
            [int(solution_object.__peer_signed_ephermal_pub__[-1]) ^ 1])
        solution_object.__peer_signed_ephermal_pub__ = forged_psep
        print("Testing forged signature")
        ver1 = solution_object.receive_ephermal_pubkey()
        solution_object.__peer_signed_ephermal_pub__ = psep
        ver2 = solution_object.receive_ephermal_pubkey()

        if (not ver1 and ver2 and isinstance(solution_object.peer_ephermal_pubkey, PublicKey)):
            step5_pass = True
    except Exception as E:
        print(E)
        step5_pass = False

    if not step5_pass:
        print(
            "Step 5 failed: Please check self.receive_ephermal_pubkey() if you are correctly verifying the signature after receiving the peer's signed ephermal public key.")

    step6_pass = False
    try:
        solution_object.perform_ecdh_keyexchange()
        if isinstance(solution_object.ECDH_box, Box):
            step6_pass = True
    except Exception as E:
        print(E)
        step6_pass = False

    if not step6_pass:
        print(
            "Step 6 failed: Please check the self.perform_ecdh_keyexchange() function and that you are setting the self.ECDH_box variable correctly.")

    return solution_object, [step1_pass,
                             step2_pass,
                             step3_pass,
                             step4_pass,
                             step5_pass,
                             step6_pass]


def check_solution_A():
    solution_object, pass_tuple = check_solution(Solution_A())
    try:

        step7_pass = abs(2 - float(solution_object.decrypt(solution_object.seller_decrypt_purchase_request(
            solution_object.encrypt(
                '{"charging_start": 1618056000, "charging_end": 1618059600, "charging_duration": 3600, "charging_station_name": "Charging Station 1", "energy_provider_name": "Energy Provider 2", "battery_energy_before": 0, "battery_energy_after": 10, "energy_bought": 10, "price":null }'.encode(
                    'utf-8')))).decode('utf-8'))) <= 0.01

        if not step7_pass:
            "Step 7 failed: Please check if the self.encrypt(), self.decrypt() and the self.seller_decrypt_purchase_request() functions are implemented correctly, and that you are accurately computing the price for the energy."

        return pass_tuple + [step7_pass]

    except Exception as E:
        print(E)
        print("Step 7 failed")
        return tuple(pass_tuple + [False])


def evaluation():
    """
    This method computes the evaluation based on a weighting factor
    """
    weighting_a = (.2, .1, .1, .15, .15, .1, .2)

    evaluation_A = 0
    try:
        for (success, weight) in zip(check_solution_A(), weighting_a):
            if success:
                evaluation_A += weight
    except Exception as E:
        print("Scenario A task failed to run:")
        print(E)

    return (evaluation_A * 100,)


e = evaluation()

print(f"Grade = {e[0]}%")

if e[0] == 100:
    print("Perfect Score")
