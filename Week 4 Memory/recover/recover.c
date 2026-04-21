#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }
    char *Input = argv[1];

    if (Input == NULL)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    typedef uint8_t BYTE;
    BYTE buffer[BLOCK_SIZE];
    int counter = 0;
    int bytes = 0;

    //PSEUDOCODE

    //Open Memory Card
    FILE *f = fopen(Input, "r");
    FILE *img = NULL;

    // Repeat Until end of file
    while (1)
    {
        //read 512 Bytes into a buffer
        bytes = fread(buffer, sizeof(BYTE), BLOCK_SIZE, f);
        //if start of new jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if first jpeg
            if (counter == 0)
            {
                //create file and write to file
                sprintf(Input, "%03i.jpg", counter);
                img = fopen(Input, "w");
                fwrite(buffer, sizeof(BYTE), bytes, img);
                counter++;
            }
            //Else
            else
            {
                // close the file and open new file to write to
                fclose(img);
                sprintf(Input, "%03i.jpg", counter);
                img = fopen(Input, "w");
                fwrite(buffer, sizeof(BYTE), bytes, img);
                counter++;
            }
        }
        //else
        //if already found Jpeg
        else if (counter != 0)
        {
            //... keep writing to it, and it might occur multiple times
            fwrite(buffer, sizeof(BYTE), bytes, img);
            if (bytes == 0)
            {
                // if end of file reached, close file
                fclose(img);
                fclose(f);
                return 0;;
            }
        }
    }
}

