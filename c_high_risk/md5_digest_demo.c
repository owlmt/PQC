// Very high risk: MD5 for integrity. Collisions are practical.
#include <openssl/md5.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    const unsigned char msg[] = "MD5 legacy demo";
    unsigned char dgst[MD5_DIGEST_LENGTH];
    MD5(msg, strlen((const char*)msg), dgst);
    for (int i = 0; i < MD5_DIGEST_LENGTH; i++) printf("%02x", dgst[i]);
    printf("  MD5 digest\n");
    return 0;
}
