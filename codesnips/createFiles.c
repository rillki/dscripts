#include <stdio.h>
#include <stdlib.h>

int main(void) {
    char str[512];
    char *male = "0 0 0 1 1";
    char *female = "1 0 0 1 1";

    //12787
    for(int i = 1; i < 12787; i++) {
	snprintf(str, sizeof(str), "%d.txt", i);
	
	FILE *fp = fopen(str, "w");
	
	fprintf(fp, "%s", (i > 6151 ? female : male));

	fclose(fp);
    }
}
