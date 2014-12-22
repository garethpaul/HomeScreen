//
//  TweepPicture
//

import Foundation
import TwitterKit

func TweepPicture(handle: String, completion: (result: String) -> Void) {

    typealias JSON = AnyObject
    typealias JSONDictionary = Dictionary<String, JSON>
    typealias JSONArray = Array<JSON>

    // Setup endpoint for retrieving the user's photo
    let restEndpoint = "https://api.twitter.com/1.1/users/show.json"

    // Setup params e.g. screen_name : gpj
    let params = ["screen_name": handle]

    // Container for errors
    var clientError : NSError?

    // Initialize Twitter
    Twitter.initialize()

    // Setup the request to send to twitter
    let request = Twitter.sharedInstance().APIClient.URLRequestWithMethod("GET", URL:  restEndpoint, parameters: params, error:&clientError)

    // If the request is valid
    if request != nil {

        // Send Request to Twitter REST Api.
        Twitter.sharedInstance().APIClient.sendTwitterRequest(request) {
            (response, data, connectionError) -> Void in
            if (connectionError == nil) {
                var jsonError : NSError?

                // Setup json to contain the JSON object returned by the API
                let json : AnyObject? = NSJSONSerialization.JSONObjectWithData(data, options: nil, error: &jsonError)

                // find the profile image from the json object e.g. {"profile_image_url": ...}
                let profile_image_url = json!["profile_image_url"] as? String

                // Complete and return the profile_image_url back.
                completion(result: String(profile_image_url!))
            }

            else {
                println("Error: \(connectionError)")
            }
        }
    }
    else {
        println("Error: \(clientError)")
    }
    
}