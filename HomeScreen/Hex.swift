//
//  Hex.swift
//

import Foundation
import UIKit

// Converts a hex string into a UIColor
//
func toColor (hex:String) -> UIColor {
    var cString:String = hex.stringByTrimmingCharactersInSet(NSCharacterSet.whitespaceAndNewlineCharacterSet() as NSCharacterSet).uppercaseString

    if (cString.hasPrefix("#")) {
        cString = cString.substringFromIndex(advance(cString.startIndex, 1))
    }

    if (countElements(cString) != 6) {
        return UIColor.grayColor()
    }

    var rgbValue:UInt32 = 0
    let scanner = NSScanner(string: cString)
    if !scanner.scanHexInt(&rgbValue) || !scanner.atEnd {
        return UIColor.grayColor()
    }

    return UIColor(
        red: CGFloat((rgbValue & 0xFF0000) >> 16) / 255.0,
        green: CGFloat((rgbValue & 0x00FF00) >> 8) / 255.0,
        blue: CGFloat(rgbValue & 0x0000FF) / 255.0,
        alpha: CGFloat(1.0)
    )
}
