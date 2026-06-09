//
//  URL.swift
//  location_tracker
//

import Foundation
import UIKit

class URL{

    func downloadImage(url: NSURL, handler: ((image: UIImage?, NSError!) -> Void))
    {
        var imageRequest: NSURLRequest = NSURLRequest(URL: url)
        NSURLConnection.sendAsynchronousRequest(imageRequest,
            queue: NSOperationQueue.mainQueue(),
            completionHandler:{response, data, error in
                if let imageData = data {
                    if let image = UIImage(data: imageData) {
                        handler(image: image, error)
                        return
                    }
                }
                handler(image: nil, error)
        })
    }

    func post(params : String, url : String, postCompleted : (succeeded: Bool, msg: String) -> ()) {
        if let requestURL = NSURL(string: url) {
            var request = NSMutableURLRequest(URL: requestURL)
            var session = NSURLSession.sharedSession()
            request.HTTPMethod = "POST"

            var err: NSError?
            var bodyData = params
            request.HTTPBody = bodyData.dataUsingEncoding(NSUTF8StringEncoding);
            var task = session.dataTaskWithRequest(request, completionHandler: {data, response, error -> Void in
                //println("Response: \(response)")
                if let responseData = data {
                    var strData = NSString(data: responseData, encoding: NSUTF8StringEncoding)
                    //println("Body: \(strData)")
                    var err: NSError?
                    var json = NSJSONSerialization.JSONObjectWithData(responseData, options: .MutableLeaves, error: &err) as? NSDictionary
                    postCompleted(succeeded: err == nil, msg: err == nil ? "OK" : "Invalid response")
                } else {
                    postCompleted(succeeded: false, msg: "Missing response data")
                }
            })
            task.resume()
        } else {
            postCompleted(succeeded: false, msg: "Invalid URL")
        }
    }
}
