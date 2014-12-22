//
//  RBResizer.swift
//  Locker
//
//  Created by Hampton Catlin on 6/20/14 and amended by Gareth Paul Jones for circular images.

import UIKit

func RBSquareImageTo(image: UIImage, size: CGSize) -> UIImage {
    return RBResizeImage(RBSquareImage(image), size)
}

func RBSquareImage(image: UIImage) -> UIImage {
    var originalWidth  = image.size.width
    var originalHeight = image.size.height

    var edge: CGFloat
    if originalWidth > originalHeight {
        edge = originalHeight
    } else {
        edge = originalWidth
    }

    var posX = (originalWidth  - edge) / 2.0
    var posY = (originalHeight - edge) / 2.0

    var cropSquare = CGRectMake(posX, posY, edge, edge)

    var imageRef = CGImageCreateWithImageInRect(image.CGImage, cropSquare);
    return UIImage(CGImage: imageRef, scale: UIScreen.mainScreen().scale, orientation: image.imageOrientation)!
}

func CircleImage(image: UIImage) -> UIImage {
    let size = image.size;
    UIGraphicsBeginImageContextWithOptions(CGSizeMake(size.width, size.height), false, 0.0)
    let context = UIGraphicsGetCurrentContext();
    //Get the width and heights
    let imageWidth = size.width;
    let imageHeight = size.height;

    //Calculate the scale factor
    let scaleFactorX = 1
    let scaleFactorY = 1

    //Calculate the centre of the circle
    let imageCentreX = imageWidth/2;
    let imageCentreY = imageHeight/2;

    // Create and CLIP to a CIRCULAR Path
    // (This could be replaced with any closed path if you want a different shaped clip)
    let radius = imageWidth/2;

    //
    CGContextBeginPath(context)
    CGContextAddArc(context, imageCentreX, imageCentreY, radius, 0, 2*3.14159265, 0)
    CGContextClip(context);
    //    CGContextScaleCTM (context, )

    let rect = CGRectMake(0, 0, size.width, size.height)
    image.drawInRect(rect)


    let newImage = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();



    return newImage
}

func RBResizeImage(image: UIImage, targetSize: CGSize) -> UIImage {
    let size = image.size

    let widthRatio  = targetSize.width  / image.size.width
    let heightRatio = targetSize.height / image.size.height

    // Figure out what our orientation is, and use that to form the rectangle
    var newSize: CGSize
    if(widthRatio > heightRatio) {
        newSize = CGSizeMake(size.width * heightRatio, size.height * heightRatio)
    } else {
        newSize = CGSizeMake(size.width * widthRatio,  size.height * widthRatio)
    }

    // This is the rect that we've calculated out and this is what is actually used below

    let rect = CGRectMake(0, 0, newSize.width, newSize.height)


    // Actually do the resizing to the rect using the ImageContext stuff
    UIGraphicsBeginImageContextWithOptions(newSize, false, 1.0)

    image.drawInRect(rect)

    let newImage = UIGraphicsGetImageFromCurrentImageContext()
    UIGraphicsEndImageContext()
    
    return newImage
}