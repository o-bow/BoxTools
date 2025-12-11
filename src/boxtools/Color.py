#!/usr/bin/env python3

class ShellColor:
    # Foreground:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    # Formatting
    # or https://misc.flogisoft.com/bash/tip_colors_and_formatting
    # note: -e does nothing special on osx (no idea about why)
    RED = '\033[31m'
    BRIGHT_GREEN_BGD = "\033[102m"
    CYAN_BGD = "\033[106m"
    RED_BGD = "\033[1;41m"
    YELLOW_BGD = "\033[1;43m"
    BLUE_BGD = "\033[44m"
    CUSTOM_BLUE_BGD = "\033[48;5;39m"
    PURPLE_BGD = "\033[1;45m"
    LIGHT_GRAY_TXT = "\033[37m"
    CYAN_TXT = "\033[36m"
    PURPLE_TXT = "\033[35m"
    BLUE_TXT = "\033[34m"
    ORANGE_TXT = "\033[33m"
    GREEN_TXT = "\033[32m"
    RED_TXT = "\033[31m"
    BLACK_TXT = "\033[30m"
    LIGHT_GREEN_TXT = "\033[92m"
    WHITE_TXT = "\033[97m"

    C_PALE_WHITE_TXT = "\033[38;5;252m"
    C_BG_BLUE_TXT = "\033[48;5;19m"

    FORCED_BLACK = "\033[38;5;235m"

    EFFECT_BOLD = "\033[1m"
    EFFECT_DIM = "\033[2m"
    EFFECT_ITALIC = "\033[3m"
    EFFECT_UNDERLINE = "\033[4m"
    EFFECT_BLINKING = "\033[5m"
    EFFECT_REVERSE = "\033[7m"
    EFFECT_INVISIBLE = "\033[8m"
    # End colored text
    END = '\033[0m'
    NC = '\x1b[0m'  # No Color

    #Mise en forme du texte dans le terminal
    #0 texte normal, sans style particulier ni couleur
    #1 gras, brillant
    #2 de faible intensité
    #4 souligné
    #5 clignotant (ne fonctionne pas sur tous les terminaux)
    #7 échanger les couleurs du texte et de l’arrière-plan
    #8 caché
    #39 couleur par défaut du texte
    #49 couleur par défaut de l’arrière-plan
    #30–37 et 90–97 des couleurs simples pour le texte
    #40–47 et 100–107 des couleurs simples pour l’arrière-plan
    #38 ;5 ;0–255 256 couleurs possibles pour le texte
    #48 ;5 ;0–255 256 couleurs possibles pour l’arrière-plan
    #38 ;2 ;0–255 ;0–255 ;0–255 couleurs pour le texte en RGB (Red Green Blue)
    #48 ;2 ;0–255 ;0–255 ;0–255 couleurs pour l’arrière-plan en RGB



class ANSICompatible:
    END = '\x1b[0m'

    # If foreground is False that means color effect is on Background
    @staticmethod
    def color(color_no, foreground=True):  # 0 - 255
        fb_g = 38  # Effect on foreground
        if not foreground:
            fb_g = 48  # Effect on background
        return '\x1b[' + str(fb_g) + ';5;' + str(color_no) + 'm'


class Formatting:
    Bold = "\x1b[1m"
    Dim = "\x1b[2m"
    Italic = "\x1b[3m"
    Underlined = "\x1b[4m"
    Blink = "\x1b[5m"
    Reverse = "\x1b[7m"
    Hidden = "\x1b[8m"
    # Reset part
    Reset = "\x1b[0m"
    Reset_Bold = "\x1b[21m"
    Reset_Dim = "\x1b[22m"
    Reset_Italic = "\x1b[23m"
    Reset_Underlined = "\x1b[24"
    Reset_Blink = "\x1b[25m"
    Reset_Reverse = "\x1b[27m"
    Reset_Hidden = "\x1b[28m"


class GColor:  # Gnome supported
    END = "\x1b[0m"

    # If Foreground is False that means color effect on Background
    @staticmethod
    def rgb(r, g, b, foreground=True):  # R: 0-255  ,  G: 0-255  ,  B: 0-255
        fb_g = 38  # Effect on foreground
        if not foreground:
            fb_g = 48  # Effect on background
        return "\x1b[" + str(fb_g) + ";2;" + str(r) + ";" + str(g) + ";" + str(b) + "m"


class Color:
    # Foreground
    F_Default = "\x1b[39m"
    F_Black = "\x1b[30m"
    F_Red = "\x1b[31m"
    F_Green = "\x1b[32m"
    F_Yellow = "\x1b[33m"
    F_Blue = "\x1b[34m"
    F_Magenta = "\x1b[35m"
    F_Cyan = "\x1b[36m"
    F_LightGray = "\x1b[37m"
    F_DarkGray = "\x1b[90m"
    F_LightRed = "\x1b[91m"
    F_LightGreen = "\x1b[92m"
    F_LightYellow = "\x1b[93m"
    F_LightBlue = "\x1b[94m"
    F_LightMagenta = "\x1b[95m"
    F_LightCyan = "\x1b[96m"
    F_White = "\x1b[97m"
    # Background
    B_Default = "\x1b[49m"
    B_Black = "\x1b[40m"
    B_Red = "\x1b[41m"
    B_Green = "\x1b[42m"
    B_Yellow = "\x1b[43m"
    B_Blue = "\x1b[44m"
    B_Magenta = "\x1b[45m"
    B_Cyan = "\x1b[46m"
    B_LightGray = "\x1b[47m"
    B_DarkGray = "\x1b[100m"
    B_LightRed = "\x1b[101m"
    B_LightGreen = "\x1b[102m"
    B_LightYellow = "\x1b[103m"
    B_LightBlue = "\x1b[104m"
    B_LightMagenta = "\x1b[105m"
    B_LightCyan = "\x1b[106m"
    B_White = "\x1b[107m"


# Sample

#if __name__ == '__main__':
#    print("Base:")
#    print(Base.FAIL,"This is a test!", Base.END)
#
#    print("ANSI_Compatible:")
#    print(ANSI_Compatible.Color(120),"This is a test!", ANSI_Compatible.END)
#
#    print("Formatting:")
#    print(Formatting.Bold,"This is a test!", Formatting.Reset)
#
#    print("GColor:") # Gnome terminal supported
#    print(GColor.RGB(204,100,145),"This is a test!", GColor.END)
#
#    print("Color:")
#    print(Color.F_Cyan,"This is a test!",Color.F_Default)