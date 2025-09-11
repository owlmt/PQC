// High risk: RC4 stream cipher with a static key. Known biases and broken in practice.
#include <openssl/rc4.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    const unsigned char key[16] = "STATIC_RC4_KEY";
    const unsigned char msg[] = "RC4 legacy demo";
    unsigned char ct[sizeof msg], pt[sizeof msg];

    RC4_KEY k; RC4_set_key(&k, (int)sizeof key, key);
    RC4(&k, (unsigned long)sizeof msg, msg, ct);

    RC4_set_key(&k, (int)sizeof key, key);
    RC4(&k, (unsigned long)sizeof msg, ct, pt);

    printf("RC4 decrypted: %s\n", pt);
    return 0;
}
