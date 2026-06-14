//
//
//  Created by Gareth Jones  on 12/14/14.
//  Copyright (c) 2014 Twitter. All rights reserved.
//


import Foundation
import TwitterKit

func UpdateStatus(status: String, mediaId: String,
    completion: (succeeded: Bool) -> Void) {

    // setup some type aliases to handle regular wording for JSON type objects
    typealias JSON = AnyObject
    typealias JSONDictionary = Dictionary<String, JSON>
    typealias JSONArray = Array<JSON>

    // set an endpoint you can check out the docs via:
    // https://dev.twitter.com/rest/reference/post/statuses/update
    let RESTAPIEndpoint = "https://api.twitter.com/1.1/statuses/update.json"

    // setup the params for the request
    let params = ["status": status, "media_ids": mediaId]

    // setup container for an error
    var clientError : NSError?

    // get the TwitterAPI client
    var twAPIClient = Twitter.sharedInstance().APIClient

    // ready the post request for magic
    var twUploadRequest = twAPIClient.URLRequestWithMethod("POST", URL: RESTAPIEndpoint, parameters: params, error: &clientError)

    // if the post request is ready for prime time
    if twUploadRequest != nil {

        // send post request to Twitter
        twAPIClient.sendTwitterRequest(twUploadRequest) {
            (response, data, connectionError) -> Void in
            if (connectionError == nil) {

                if let responseData = data {
                    var jsonError : NSError?
                    let json : AnyObject? =
                    NSJSONSerialization.JSONObjectWithData(responseData,
                        options: nil,
                        error: &jsonError)
                    if let jsonDictionary = json as? JSONDictionary {
                        if let statusID = jsonDictionary["id_str"] as? String {
                            let trimmedStatusID = statusID.stringByTrimmingCharactersInSet(
                                NSCharacterSet.whitespaceAndNewlineCharacterSet())
                            if !trimmedStatusID.isEmpty {
                                completion(succeeded: true)
                                return
                            }
                        }
                    }
                }
            }
            completion(succeeded: false)
        }
    } else {
        completion(succeeded: false)
    }
}

