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
        let userName = Twitter.sharedInstance().session().userName;
        // we need pictures then we are good
        TweepPicture(userName){ (result: String) in

            let url = URL()
            let url_string = result
            url.downloadImage(NSURL(string: url_string)!, {image, error in
                let newImg = image
                let circle = CircleImage(RBResizeImage(newImg, CGSize(width: 100, height: 100)))
                self.profilePic!.image = circle
                self.profilePic.hidden = true
            })
        }

        if getNumberOfImages() == true {
            let screenObj = CGSize(width:self.screenSize.width*2, height: self.screenSize.height*2)
            // get Screenshot
            getScreenshotImage(screenObj) { (result: UIImage) in
                self.screenImage.image = result
                //self.homeScreen.image = result
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
        let media: NSData = UIImageJPEGRepresentation(self.screenImage.image, 100)

        // Upload the data to uploads.twitter.com and then use the media_id to update status
        UploadMedia(media) { (media_id: String) in
            UpdateStatus(text, media_id)
        }

        // Send the user back to the initial "main" screen
        self.performSegueWithIdentifier("cancelSegue", sender: self)

    }

    // Close the share controller
    //
    func close(){
        self.view.endEditing(true)

        // Send the user back to the initial "main" screen
        self.performSegueWithIdentifier("cancelSegue", sender: self)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    
    
    
}

