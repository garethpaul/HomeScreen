//
//
//  Created by Gareth Jones  on 12/14/14.
//  Copyright (c) 2014 Twitter. All rights reserved.
//


import Foundation
import TwitterKit

func UploadMedia(media: NSData, completion: (result: [String]) -> Void) {

    // setup some type aliases to handle regular wording for JSON type objects
    typealias JSON = AnyObject
    typealias JSONDictionary = Dictionary<String, JSON>
    typealias JSONArray = Array<JSON>

    let RESTAPIEndpoint = "https://api.twitter.com/1.1/statuses/update_with_media.json"
    let params = ["status": "SHARE YOUR HOMESCREEN", "key": "media[]", "media[]": media.base64EncodedDataWithOptions(nil), ]

    // setup container for an error
    var clientError : NSError?

    // Initialize Twitter
    Twitter.initialize()

    // Send a REQUEST to Twitter using GuestAuthentication e.g. no authenticated user just the app.
    Twitter.sharedInstance().logInWithCompletion{
        (session, error) -> Void in
        if (session != nil) {

            // woohoo we have a session - let's get crazy
            let request = Twitter.sharedInstance().APIClient.URLRequestWithMethod("POST", URL:  RESTAPIEndpoint, parameters: params, error:&clientError)

            // if the request is ready to rock and roll
            if request != nil {

                // let's send us a REST API reuest
                Twitter.sharedInstance().APIClient.sendTwitterRequest(request) {
                    (response, data, connectionError) -> Void in
                    if (connectionError == nil) {

                        var jsonError : NSError?
                        let json : AnyObject? =
                        NSJSONSerialization.JSONObjectWithData(data,
                            options: nil,
                            error: &jsonError)

                        // Iterate through JSON response and append the values to the TweetArray

                        println(json)
                        // complete this magical request
                        //completion(result: tweetArray)
                    }



                    else {
                        println("Error: \(connectionError)")
                    }
                }
            }
            else {
                println("Error: \(clientError)")
            }
            
        } else {
            println("error: \(error.localizedDescription)");
        }
        
    }
}



