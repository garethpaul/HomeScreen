//
//
//  Created by Gareth Jones  on 12/14/14.
//

import Foundation
import TwitterKit

func Search(completion: (result: [String]) -> Void) {

    // setup some type aliases to handle regular wording for JSON type objects
    typealias JSON = AnyObject
    typealias JSONDictionary = Dictionary<String, JSON>
    typealias JSONArray = Array<JSON>

    // set an endpoint you can check out the docs via:
    // https://dev.twitter.com/rest/reference/get/search/tweets
    let RESTAPIEndpoint = "https://api.twitter.com/1.1/search/tweets.json"

    // setup the params for the request
    let params = ["q": "#homescreen", "count": "15"]

    // setup container for an error
    var clientError : NSError?

    // Initialize Twitter
    Twitter.initialize()

    // Send a REQUEST to Twitter using GuestAuthentication e.g. no authenticated user just the app.
    Twitter.sharedInstance().logInWithCompletion{
        (session, error) -> Void in
        if (session != nil) {

            // woohoo we have a session - let's get crazy
            let request = Twitter.sharedInstance().APIClient.URLRequestWithMethod("GET", URL:  RESTAPIEndpoint, parameters: params, error:&clientError)

            // if the request is ready to rock and roll
            if request != nil {

                // let's send us a REST API reuest
                Twitter.sharedInstance().APIClient.sendTwitterRequest(request) {
                    (response, data, connectionError) -> Void in
                    if (connectionError == nil) {

                        // Setup a tweet array to contain all of those juicy tweets
                        var tweetArray = Array<String>()

                        var jsonError : NSError?
                        let json : AnyObject? =
                        NSJSONSerialization.JSONObjectWithData(data,
                            options: nil,
                            error: &jsonError)

                        // Iterate through JSON response and append the values to the TweetArray
                        if let statuses = json!["statuses"] as? JSONArray {

                            // For each tweet in the status block of the json request e.g. {"statuses": [tweets.........
                            for tweet in statuses {
                                if let id = tweet["id_str"] as?String{

                                    // Append the Tweet to the array
                                    tweetArray.append(id)
                                }
                            }
                        }

                        // complete this magical request
                        completion(result: tweetArray)
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



