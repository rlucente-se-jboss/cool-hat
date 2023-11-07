#!/usr/bin/env python3

# Based on BASIC code from a 1981 Commodore PET ad but this version scales to
# any size.  Example:
#
# hat [yields hat that is 320x200]
#
# hat -w 1000 [hat 1000 pixels wide, 2x64 slices]
#
# hat -w 1000 -s 10 [1000 pixels wide, 2x10 slices]
#
# Mike Markowski, mike.ab3ap@gmail.com
# April 2022
#
# Modified November 2023 to simply add a band to the hat.

from PIL import Image, ImageDraw
import numpy as np
import sys

def hat(scrX=320, nSlices=64):
    # Original values from Commodore PET ad.
    x0 = 320; y0 = 200 # Screen res math originally targeted.
    r0 = 144           # Radius of hat.
    h0 = 56            # Height of hat.
    n0 = 64            # Number of slices, 2x64 total.
    a0 = 3 * np.pi/2   # Max angle of sinusoidal to revolve, 270 deg.

    # New values for any size hat.
    scrY = round(scrX * y0/x0) # Height, using old screen ratio.
    fg = 'red'; bg = 'black' # Fond memories of CRTs.  :-)
    hatHgt  = h0/y0 * scrY     # New hat height.
    hatRad  = r0/x0 * scrX     # New hat radius.
    stagger = n0/x0 * scrX     # Scale layer stagger for fake 3d.
    xf      = a0 / hatRad      # Radians per vertical point on hat.

    bandInner =  98 * scrX/x0  # trial/error based on 144 above then scaled
    bandOuter = 106 * scrX/x0

    # Make the hat!
    img = Image.new('RGB', (scrX, scrY))
    w = ImageDraw.Draw(img)
    for zSlice in np.arange(-1, 1, 1/nSlices): # Slices, back to front.
        z = zSlice * hatRad                    # -hatRad to hatRad.
        xl = round(np.sqrt(hatRad**2 - z**2))  # Endpoints of hat, this slice.
        for x in range(-xl, xl+1):             # Step through points on slice.
            r = np.sqrt(x*x + z*z)             # Add a band to the hat
            if r < bandInner or r > bandOuter: # Use radius to define "band"
                # Hat-like surface of revolution.
                xt = xf * np.sqrt(x**2 + z**2)     # Dist along hat's sinusoid.
                y = (np.sin(xt) + 0.4*np.sin(xt*3)) * hatHgt # Pt on hat.
                # Stagger layer for fake 3d.
                x1 = x + stagger*zSlice + scrX/2
                y1 = y - stagger*zSlice + scrY/2
                y1 = scrY - y1 # Flip vertically.
                w.point((x1, y1), fill=fg)
                w.line([(x1, y1+1), (x1, scrY-1)], fill=bg) # Erase prev layer.
    img.save('hat.png')
    img.show()

def cliArgs(argv):
    '''Parse command line arguments.
    '''
    nSlices = 64 # Default, 2x64 slices.
    scrX = 320   # Default, 320 pixels wide.
    i = 0
    while i < len(argv):
        if argv[i] == '-s': # Number of slices in hat.
            i += 1
            nSlices = int(argv[i])
        elif argv[i] == '-w': # Pixel width of image.
            i += 1
            scrX = int(argv[i])
        else:
            usage()
        i += 1
    return scrX, nSlices

def usage():
    print('hat [-w width] [-s slices]')
    print('    -s slices : create hat with 1 + (2 x slices)')
    print('    -w width : width of resulting image in pixels')
    sys.exit(1)

def main(argv):
    scrX, nSlices = cliArgs(argv[1:])
    hat(scrX, nSlices)

if __name__ == '__main__':
    main(sys.argv)

