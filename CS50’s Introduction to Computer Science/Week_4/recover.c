#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check for correct usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the forensic image
    FILE *image = fopen(argv[1], "r");
    if (!image)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    // Create a buffer for a block of data
    BYTE buffer[512];

    // Initialize variables for file name and count
    char filename[8];
    int count = 0;
    FILE *output = NULL;

    // While there's still data left to read from the forensic image
    while (fread(buffer, 1, 512, image) == 512)
    {
        // Check for the beginning of a JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG file is already open, close it
            if (output != NULL)
            {
                fclose(output);
            }

            // Create a new JPEG file
            sprintf(filename, "%03d.jpg", count);
            output = fopen(filename, "w");
            if (!output)
            {
                fclose(image);
                printf("Could not create %s.\n", filename);
                return 1;
            }

            // Write the data to the new JPEG file
            fwrite(buffer, 1, 512, output);
            count++;
        }
        // If a JPEG file is already open, write the data to it
        else if (output != NULL)
        {
            fwrite(buffer, 1, 512, output);
        }
    }

    // Close the forensic image file
    fclose(image);

    // Close the last JPEG file
    if (output != NULL)
    {
        fclose(output);
    }

    return 0;
}
