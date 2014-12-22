//
//  TweetsController.swift
//

import UIKit
import TwitterKit

class TweetsController: UITableViewController, TWTRTweetViewDelegate  {

    // setup Variables
    var lView: UIImageView!
    var container: UIView!
    var label: UILabel!


    let activityIndicator: UIActivityIndicatorView = UIActivityIndicatorView(activityIndicatorStyle: UIActivityIndicatorViewStyle.Gray)

    @IBOutlet var textLabel: UILabel!

    // setup a 'container' for Tweets
    var tweets: [TWTRTweet] = [] {
        didSet {
            tableView.reloadData()
        }
    }

    var prototypeCell: TWTRTweetTableViewCell?

    let tweetTableCellReuseIdentifier = "TweetCell"

    var isLoadingTweets = false
    var prev: Int?


    override func viewDidLoad() {
        super.viewDidLoad()

        // setup the View
        self.setupView()

        self.navigationItem.setHidesBackButton(true, animated:true);
    }

    func setupView(){

        // 
        lView = UIImageView(frame: CGRectMake(0, 0, 29.8, 33))
        lView.image = UIImage(named: "logo")?.imageWithRenderingMode(.AlwaysTemplate)
        lView.tintColor = toColor("ffffff")
        lView.frame.origin.x = (self.view.frame.size.width - lView.frame.size.width) / 2
        lView.frame.origin.y = -lView.frame.size.height - 1
        self.navigationController?.view.addSubview(lView)
        self.navigationController?.view.bringSubviewToFront(lView)

        // Customize the navigation bar.
        let titleDict: NSDictionary = [NSForegroundColorAttributeName: toColor("FF9500")]
        self.navigationController?.navigationBar.titleTextAttributes = titleDict
        self.navigationController?.navigationBar.shadowImage = UIImage()
        self.navigationController?.navigationBar.topItem?.title = ""
        self.navigationController?.navigationBar.barTintColor = toColor("FF9500")
        self.navigationController?.navigationBar.tintColor = toColor("FF9500")

        // hide rows with clearColor until filled with Tweets
        container = UIView(frame: CGRectMake(0, 0, self.view.frame.size.width, 200));
        container.backgroundColor = UIColor.clearColor()
        self.tableView.tableFooterView = container

        // put a spinner on the loading and waiting
        activityIndicator.frame = CGRectMake(100, 100, 100, 100);
        activityIndicator.frame.origin.x = (self.view.frame.size.width - activityIndicator.frame.size.width) / 2
        activityIndicator.frame.origin.y = (self.view.frame.size.height/2) - 100
        activityIndicator.startAnimating()
        self.activityIndicator.hidden = false
        self.view.addSubview( activityIndicator )


        // Create a single prototype cell for height calculations.
        self.prototypeCell = TWTRTweetTableViewCell(style: .Default, reuseIdentifier: tweetTableCellReuseIdentifier)

        // Register the identifier for TWTRTweetTableViewCell.
        self.tableView.registerClass(TWTRTweetTableViewCell.self, forCellReuseIdentifier: tweetTableCellReuseIdentifier)

        dispatch_async(dispatch_get_main_queue()) {
            // Send a request to the Search API. Check out TVSearchAPI.swift for details..
            Search() { (result: [String]) in
                // Load the array back to display the Tweets
                self.loadTweets(result)
            }



        }




    }

    func loadTweets(tweetIDs: [String]) {
        // Do not trigger another request if one is already in progress.
        if self.isLoadingTweets {
            return
        }

        // load tweets with guest login
        Twitter.sharedInstance().logInGuestWithCompletion { (session: TWTRGuestSession!, error: NSError!) in

            // Find the tweets with the tweetIDs
            Twitter.sharedInstance().APIClient.loadTweetsWithIDs(tweetIDs) {
                (twttrs, error) -> Void in

                // If there are tweets do something magical
                if ((twttrs) != nil) {

                    // Loop through tweets and do something
                    for i in twttrs {
                        // Append the Tweet to the Tweets to display in the table view.
                        self.tweets.append(i as TWTRTweet)
                    }
                } else {
                    println(error)
                }
                // once loaded

                // Stop animating the spinner
                self.activityIndicator.stopAnimating()

                // Remove the spinner
                self.activityIndicator.hidden = true

            }
        }

    }


    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }




    func refreshInvoked() {
        // Trigger a load for the most recent Tweets.
        Search() { (result: [String]) in
            self.loadTweets(result)
        }
    }

    // MARK: TWTRTweetViewDelegate
    func tweetView(tweetView: TWTRTweetView!, didSelectTweet tweet: TWTRTweet!) {
        // Display a Web View when selecting the Tweet.
        let webViewController = UIViewController()
        let webView = UIWebView(frame: webViewController.view.bounds)
        webView.loadRequest(NSURLRequest(URL: tweet.permalink))
        webViewController.view = webView
        self.navigationController?.pushViewController(webViewController, animated: true)
    }


    // MARK: UITableViewDataSource
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // Return the number of Tweets.


        return tweets.count
    }

    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        // Retrieve the Tweet cell.
        let cell = tableView.dequeueReusableCellWithIdentifier(tweetTableCellReuseIdentifier, forIndexPath: indexPath) as TWTRTweetTableViewCell



        // Assign the delegate to control events on Tweets.
        cell.tweetView.delegate = self

        // Retrieve the Tweet model from loaded Tweets.
        let tweet = tweets[indexPath.row]

        // Configure the cell with the Tweet.
        cell.configureWithTweet(tweet)

        // Return the Tweet cell.
        return cell
    }

    // MARK: UITableViewDelegate
    override func tableView(tableView: UITableView, heightForRowAtIndexPath indexPath: NSIndexPath) -> CGFloat {


        let tweet = self.tweets[indexPath.row]
        self.prototypeCell?.configureWithTweet(tweet)
        if let height = self.prototypeCell?.calculatedHeightForWidth(self.view.bounds.width) {
            return height
        } else {
            return self.tableView.estimatedRowHeight
        }
    }

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)

        // Animate the logo when the view appears.
        UIView.animateWithDuration(0.6, delay: 0, usingSpringWithDamping: 0.5, initialSpringVelocity: 0.8, options: .CurveEaseInOut, animations: { () -> Void in
            // Place the frame at the correct origin position.
            self.lView.frame.origin.y = 22
            }, completion: nil)
    }

    override func viewDidAppear(animated: Bool) {
        super.viewDidAppear(animated)
        
        // Make sure the navigation bar is translucent.
        self.navigationController?.navigationBar.translucent = true
    }
    
    func refreshView(){
        self.viewDidLoad()
        self.viewWillAppear(true)
    }

}

