//
//  View.swift
//

import Foundation
import UIKit

class View: UIView {

    /* 1 */
    //  override func drawRect(rect: CGRect) {
    //
    //    /* Create the path first. Just the path handle. */
    //    let path = CGPathCreateMutable()
    //
    //    /* Here are our rectangle boundaries */
    //    let rectangle = CGRect(x: 10, y: 30, width: 200, height: 300)
    //
    //    /* Add the rectangle to the path */
    //    CGPathAddRect(path, nil, rectangle)
    //
    //    /* Get the handle to the current context */
    //    let currentContext = UIGraphicsGetCurrentContext()
    //
    //    /* Add the path to the context */
    //    CGContextAddPath(currentContext, path)
    //
    //    /* Set the fill color to cornflower blue */
    //    UIColor(red: 0.20, green: 0.60, blue: 0.80, alpha: 1.0).setFill()
    //
    //    /* Set the stroke color to brown */
    //    UIColor.brownColor().setStroke()
    //
    //    /* Set the line width (for the stroke) to 5 */
    //    CGContextSetLineWidth(currentContext, 5)
    //
    //    /* Stroke and fill the path on the context */
    //    CGContextDrawPath(currentContext, kCGPathFillStroke)
    //
    //  }

    override func drawRect(rect: CGRect) {
        /* Create the path first. Just the path handle. */
        let path = CGPathCreateMutable()

        /* Here are our first rectangle boundaries */
        let rectangle1 = CGRect(x: 10, y: 30, width: 200, height: 300)

        /* And the second rectangle */
        let rectangle2 = CGRect(x: 40, y: 100, width: 90, height: 300)

        /* Put both rectangles into an array */
        let rectangles = [rectangle1, rectangle2]

        /* Add the rectangles to the path */
        CGPathAddRects(path, nil, rectangles, 2)

        /* Get the handle to the current context */
        let currentContext = UIGraphicsGetCurrentContext()

        /* Add the path to the context */
        CGContextAddPath(currentContext, path)

        /* Set the fill color to cornflower blue */
        UIColor(red: 0.20, green: 0.60, blue: 0.80, alpha: 1.0).setFill()

        /* Set the stroke color to black */
        UIColor.blackColor().setStroke()
        
        /* Set the line width (for the stroke) to 5 */
        CGContextSetLineWidth(currentContext, 5)
        
        /* Stroke and fill the path on the context */
        CGContextDrawPath(currentContext, kCGPathFillStroke)
    }
    
}