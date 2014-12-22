//
//
//  Created by Gareth Jones  on 12/14/14.
//  Copyright (c) 2014 Twitter. All rights reserved.
//


import Foundation
import TwitterKit

// Send HTTP request to upload media.
func UploadMedia(data: NSData, completion: (result: String) -> Void) {

    // setup some type aliases to handle regular wording for JSON type objects
    typealias JSON = AnyObject
    typealias JSONDictionary = Dictionary<String, JSON>
    typealias JSONArray = Array<JSON>

    // set an endpoint you can check out the docs via:
    // https://dev.twitter.com/rest/public/uploading-media
    let RESTAPIEndpoint = "https://upload.twitter.com/1.1/media/upload.json"

    // setup container for an error
    var clientError : NSError?

    var twAPIClient = Twitter.sharedInstance().APIClient
    var parameters:Dictionary = Dictionary<String, String>()

    // get image from bundle
    var imageData = data
    parameters["media"] = imageData.base64EncodedStringWithOptions(nil)

    // prepare post request to upload media
    var twUploadRequest = twAPIClient.URLRequestWithMethod("POST", URL: RESTAPIEndpoint, parameters: parameters, error: &clientError)

    // if the upload request is ready for prime time
    if twUploadRequest != nil {

        // send HTTP request to Twitter to process the media upload
        twAPIClient.sendTwitterRequest(twUploadRequest) {
            (response, data, connectionError) -> Void in
            if (connectionError == nil) {

                var jsonError : NSError?
                let json : AnyObject? =
                NSJSONSerialization.JSONObjectWithData(data,
                    options: nil,
                    error: &jsonError)
                println(json)
                if let media_id_string = json!["media_id_string"] as?String{

                    // Return media_id_string back so that the next step of magic can occur.
                    completion(result: media_id_string)
                }
                

            } else {
                println("error \(connectionError)")
            }
        }
    } else {
        println("error \(clientError)")
    }
}



