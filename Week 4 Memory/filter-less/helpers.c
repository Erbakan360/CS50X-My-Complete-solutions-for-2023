#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int Red = image[i][j].rgbtRed;
            int Green = image[i][j].rgbtGreen;
            int Blue = image[i][j].rgbtBlue;

            float x = (Red + Green + Blue) / 3.0;
            int Avg = round(x);

            image[i][j].rgbtRed = Avg;
            image[i][j].rgbtGreen = Avg;
            image[i][j].rgbtBlue = Avg;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int Red = image[i][j].rgbtRed;
            int Green = image[i][j].rgbtGreen;
            int Blue = image[i][j].rgbtBlue;

            //Calculate each new color value using the Sepia formula
            float SepR = ((Red * 0.393) + (Green * 0.769) + (Blue * 0.189));
            float SepG = ((Red * 0.349) + (Green * 0.686) + (Blue * 0.168));
            float SepB = ((Red * 0.272) + (Green * 0.534) + (Blue * 0.131));

            int SepRed = round(SepR);
            int SepGreen = round(SepG);
            int SepBlue = round(SepB);

            //Ensure the result is an integer between 0 and 255. inclusive
            if (SepRed > 255)
            {
                SepRed = 255;
            }
            else if (SepRed < 0)
            {
                SepRed = 0;
            }

            if (SepGreen > 255)
            {
                SepGreen = 255;
            }
            else if (SepGreen < 0)
            {
                SepGreen = 0;
            }

            if (SepBlue > 255)
            {
                SepBlue = 255;
            }
            else if (SepBlue < 0)
            {
                SepBlue = 0;
            }
            image[i][j].rgbtRed = SepRed;
            image[i][j].rgbtGreen = SepGreen;
            image[i][j].rgbtBlue = SepBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE Temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = Temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE Temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float TempR = 0;
            float TempG = 0;
            float TempB = 0;
            float Cell = 0;

            for (int r = -1; r < 2; r++)
            {
                for (int c = -1; c < 2; c++)
                {
                    if (i + r < 0 || i + r > height - 1)
                    {
                        continue;
                    }

                    if (j + c < 0 || j + c > width - 1)
                    {
                        continue;
                    }

                    TempB += image[i + r][j + c].rgbtBlue;
                    TempG += image[i + r][j + c].rgbtGreen;
                    TempR += image[i + r][j + c].rgbtRed;
                    Cell++;
                }
            }
            Temp[i][j].rgbtRed = round(TempR / Cell);
            Temp[i][j].rgbtGreen = round(TempG / Cell);
            Temp[i][j].rgbtBlue = round(TempB / Cell);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = Temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = Temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = Temp[i][j].rgbtBlue;
        }
    }
    return;
}