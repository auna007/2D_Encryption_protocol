// 1. Generating ECDSA Keys and Signing/Verifying

import java.security.*;
import java.security.spec.*;

// Generate ECDSA Key Pair
KeyPairGenerator g = KeyPairGenerator.getInstance("EC", "SunEC");
ECGenParameterSpec ecsp = new ECGenParameterSpec("secp224r1");
g.initialize(ecsp);

KeyPair kp = g.genKeyPair();
PrivateKey privKey = kp.getPrivate();
PublicKey pubKey = kp.getPublic();

// Signing with ECDSA
Signature s = Signature.getInstance("SHA256withECDSA", "SunEC");
s.initSign(privKey);

byte[] msg = "Hello, World!".getBytes("UTF-8");
s.update(msg);
byte[] sig = s.sign();

// Verifying the signature
Signature sg = Signature.getInstance("SHA256withECDSA", "SunEC");
sg.initVerify(pubKey);
sg.update(msg);
boolean validSignature = sg.verify(sig);


// 2. Diffie-Hellman Key Exchange


import java.math.BigInteger;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.SecureRandom;

import javax.crypto.KeyAgreement;
import javax.crypto.spec.DHParameterSpec;
import javax.crypto.spec.DHPublicKeySpec;

public class Main {
    public static void main(String[] args) throws Exception {
        BigInteger p = new BigInteger("47");
        BigInteger g = new BigInteger("71");

        SecureRandom rnd = new SecureRandom();
        p = BigInteger.probablePrime(512, rnd);
        g = BigInteger.probablePrime(512, rnd);

        createSpecificKey(p, g);
    }

    public static void createSpecificKey(BigInteger p, BigInteger g) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DiffieHellman");

        DHParameterSpec param = new DHParameterSpec(p, g);
        kpg.initialize(param);
        KeyPair kp = kpg.generateKeyPair();

        KeyFactory kfactory = KeyFactory.getInstance("DiffieHellman");
        DHPublicKeySpec kspec = (DHPublicKeySpec) kfactory.getKeySpec(kp.getPublic(), DHPublicKeySpec.class);
    }
}


// 3. AES Encryption/Decryption Using ECDH Shared Secret

import javax.crypto.*;
import javax.crypto.spec.SecretKeySpec;
import java.security.*;
import java.io.IOException;

public class AESSecurityCap {
    private PublicKey publickey;
    KeyAgreement keyAgreement;
    byte[] sharedsecret;

    String ALGO = "AES";

    AESSecurityCap() {
        makeKeyExchangeParams();
    }

    private void makeKeyExchangeParams() {
        KeyPairGenerator kpg = null;
        try {
            kpg = KeyPairGenerator.getInstance("EC");
            kpg.initialize(128);
            KeyPair kp = kpg.generateKeyPair();
            publickey = kp.getPublic();
            keyAgreement = KeyAgreement.getInstance("ECDH");
            keyAgreement.init(kp.getPrivate());

        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            e.printStackTrace();
        }
    }

    public void setReceiverPublicKey(PublicKey publickey) {
        try {
            keyAgreement.doPhase(publickey, true);
            sharedsecret = keyAgreement.generateSecret();
        } catch (InvalidKeyException e) {
            e.printStackTrace();
        }
    }

    public String encrypt(String msg) {
        try {
            Key key = generateKey();
            Cipher c = Cipher.getInstance(ALGO);
            c.init(Cipher.ENCRYPT_MODE, key);
            byte[] encVal = c.doFinal(msg.getBytes());
            return new BASE64Encoder().encode(encVal);
        } catch (BadPaddingException | InvalidKeyException | NoSuchPaddingException | IllegalBlockSizeException | NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return msg;
    }

    public String decrypt(String encryptedData) {
        try {
            Key key = generateKey();
            Cipher c = Cipher.getInstance(ALGO);
            c.init(Cipher.DECRYPT_MODE, key);
            byte[] decordedValue = new BASE64Decoder().decodeBuffer(encryptedData);
            byte[] decValue = c.doFinal(decordedValue);
            return new String(decValue);
        } catch (BadPaddingException | InvalidKeyException | NoSuchPaddingException | IllegalBlockSizeException | NoSuchAlgorithmException | IOException e) {
            e.printStackTrace();
        }
        return encryptedData;
    }

    public PublicKey getPublickey() {
        return publickey;
    }

    protected Key generateKey() {
        return new SecretKeySpec(sharedsecret, ALGO);
    }
}
