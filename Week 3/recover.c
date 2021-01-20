#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if(file == NULL)
    {
        printf("Could not open.\n");
        return 1;
    }

    int BLOCK_SIZE = 512;
    unsigned char buffer[BLOCK_SIZE];

    // out dosyası
    FILE* img = NULL;

    //JPEG Dosyası
    char image[10];

    // oluşturulan resim dosyaları numaraları
    int n = 0;

    //dosya okuma
    while(fread(buffer,BLOCK_SIZE,1,file) == 1)
    {
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            if(n > 0)
            {
                fclose(img);
            }

            //JPEG oluşturma
            sprintf(image, "%03i.jpg", n);

            // n'inci image dosyasını açma
            img = fopen(image, "w");

            if(!img)
            {
                printf("Could not open.\n");
                return 1;
            }

            // Oluşturulan imagelerin numaraları artışı
            n++;
        }
          if (img)
          {
            // image dosyası yazma
            fwrite(buffer, BLOCK_SIZE, 1, img);
          }
    }
    // dosyaları kapatma
    fclose(img);
    fclose(file);
    return 0;
}
