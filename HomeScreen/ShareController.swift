//
//  ViewController.swift
//

import UIKit
import TwitterKit
import Photos
import PhotosUI
import AssetsLibrary

class ShareController: UIViewController{

    // MARK: References
    @IBOutlet var inputText: UIView!
    @IBOutlet var inputT: UITextView!
    @IBOutlet var topView: UIView!
    @IBOutlet var navBarItem: UINavigationItem!
    @IBOutlet var profilePic: UIImageView!
    let screenSize: CGRect = UIScreen.mainScreen().bounds
    let screenImage: UIImageView = UIImageView()
    var changed = false
    var leftButton: UIImage!
    var leftView: UIImageView!
    var lBtn: UIBarButtonItem!
    var postInFlight = false
    var postGeneration = 0
    var profileGeneration = 0
    var screenshotGeneration = 0

    override func viewDidAppear(animated: Bool) {
        self.inputT.becomeFirstResponder()
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        // Show the keyboard to the user
        self.inputT.becomeFirstResponder()

        self.profilePic.hidden = true

        // Setup buttons for saving and closing
        var leftBtn = UIButton(frame: CGRect(x: 0, y: 0, width: 30, height: 30))
        leftBtn.setImage(UIImage(named: "close80"), forState: UIControlState.Normal)
        leftBtn.addTarget(self, action: Selector("close"), forControlEvents:  UIControlEvents.TouchUpInside)
        var itemL = UIBarButtonItem(customView: leftBtn)
        self.navBarItem.leftBarButtonItem?.tintColor = toColor("FFFFFF")
        self.navBarItem.leftBarButtonItem = itemL

        var rightBtn = UIButton(frame: CGRect(x: 0, y: 0, width: 30, height: 30))
        rightBtn.setImage(UIImage(named: "postBtn"), forState: UIControlState.Normal)
        rightBtn.addTarget(self, action: Selector("post"), forControlEvents:  UIControlEvents.TouchUpInside)
        var itemR = UIBarButtonItem(customView: rightBtn)
        self.navBarItem.rightBarButtonItem?.tintColor = toColor("FFFFFF")
        self.navBarItem.rightBarButtonItem = itemR

        // Hide the back button
        self.navigationItem.setHidesBackButton(true, animated:true);


        // Find the users photo
        if let session = Twitter.sharedInstance().session() {
            let userName = session.userName
            startProfileImageLoad(userName)
        }

        startScreenshotLoad()
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        invalidateProfileImageLoad()
        invalidateScreenshotLoad()
        invalidatePost()
    }

    func startProfileImageLoad(userName: String) {
        profilePic.image = nil
        profilePic.hidden = true
        profileGeneration += 1
        let generation = profileGeneration

        TweepPicture(userName){ [weak self] (result: String?) in
            NSOperationQueue.mainQueue().addOperationWithBlock { [weak self] in
                if let controller = self {
                    if controller.profileGeneration != generation {
                        return
                    }

                    if let url_string = result {
                        let url = URL()
                        if let profileURL = NSURL(string: url_string) {
                            url.downloadImage(profileURL, { [weak self] image, error in
                                if let controller = self {
                                    if controller.profileGeneration != generation {
                                        return
                                    }

                                    if let newImg = image {
                                        let circle = CircleImage(RBResizeImage(newImg, CGSize(width: 100, height: 100)))
                                        controller.profilePic!.image = circle
                                        controller.profilePic.hidden = false
                                    }
                                }
                            })
                        }
                    }
                }
            }
        }
    }

    func invalidateProfileImageLoad() {
        profileGeneration += 1
    }

    func startScreenshotLoad() {
        screenshotGeneration += 1
        let generation = screenshotGeneration

        if getNumberOfImages() == true {
            let screenObj = CGSize(width:self.screenSize.width*2, height: self.screenSize.height*2)
            getScreenshotImage(screenObj) { [weak self] (result: UIImage?) in
                if let controller = self {
                    if controller.screenshotGeneration != generation {
                        return
                    }
                    if let screenshot = result {
                        controller.screenImage.image = screenshot
                    }
                }
            }
        }
    }

    func invalidateScreenshotLoad() {
        screenshotGeneration += 1
    }

    func invalidatePost() {
        postGeneration += 1
        postInFlight = false
    }

    func completePost(generation: Int, succeeded: Bool) {
        NSOperationQueue.mainQueue().addOperationWithBlock { [weak self] in
            if let controller = self {
                if !controller.postInFlight || controller.postGeneration != generation {
                    return
                }

                controller.postInFlight = false
                if succeeded {
                    controller.performSegueWithIdentifier("cancelSegue", sender: controller)
                }
            }
        }
    }

    // Send post request to Twitter to process image with media_id
    //
    func post() {

        // End the editing
        self.view.endEditing(true)

        // Get the text from the textbox
        let text : String = inputT!.text

        // Get the home screen NSData to upload
        if let image = self.screenImage.image {
            if let media = UIImageJPEGRepresentation(image, 1.0) {
                if self.postInFlight {
                    return
                }
                self.postInFlight = true
                self.postGeneration += 1
                let generation = self.postGeneration

                // Upload the data to uploads.twitter.com and then use the media_id to update status
                UploadMedia(media) { [weak self] (media_id: String?) in
                    if let controller = self {
                        if let uploadedMediaID = media_id {
                            UpdateStatus(text, uploadedMediaID) { [weak self] (succeeded: Bool) in
                                if let controller = self {
                                    controller.completePost(generation, succeeded: succeeded)
                                }
                            }
                        } else {
                            controller.completePost(generation, succeeded: false)
                        }
                    }
                }
            }
        }

    }

    // Close the share controller
    //
    func close(){
        self.view.endEditing(true)
        invalidatePost()

        // Send the user back to the initial "main" screen
        self.performSegueWithIdentifier("cancelSegue", sender: self)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    
    
    
}
