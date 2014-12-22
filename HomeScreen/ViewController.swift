//
//  ViewController.swift
//  HomeScreen
//
//  Created by Gareth Jones  on 12/20/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import UIKit
import Photos
import PhotosUI
import AssetsLibrary
import TwitterKit

class ViewController: UIViewController, UINavigationControllerDelegate {

    // MARK: References
    @IBOutlet var homeScreen: UIImageView!


    var screenShot: UIImage!
    var shareBtn: UIButton!
    var assetLibrary : ALAssetsLibrary = ALAssetsLibrary()
    var lView: UIImageView!

    let screenSize: CGRect = UIScreen.mainScreen().bounds

    override func viewDidLoad() {
        super.viewDidLoad()

        // Setup the view to appear and make things look great
        self.setupView()

        // Get the latestImage and display to the view
        self.getLatestImage()

    }


    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        // Animate the logo when the view appears.
        UIView.animateWithDuration(0.6, delay: 0, usingSpringWithDamping: 0.5, initialSpringVelocity: 0.8, options: .CurveEaseInOut, animations: { () -> Void in
            // Place the frame at the correct origin position.
            self.lView.frame.origin.y = 22
            }, completion: nil)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    func getLatestImage(){

        // If there are images to find
        if getNumberOfImages() == true {

            // Get the screenSize
            let screenObj = CGSize(width:screenSize.width*2, height: screenSize.height*2)

            // get Screenshot if the last known screen shot appears to be valid
            getScreenshotImage(screenObj) { (result: UIImage) in

                // set some images
                self.homeScreen.image = result
                self.screenShot = result
                self.homeScreen.hidden = false
            }
        } else {

            // show the default image
            showDefault()
        }
    }

    func showDefault(){

        // display the image iPhone
        var image : UIImage = UIImage(named:"iPhone")!
        self.homeScreen.image = image
    }

    func applicationBecameActive(notification: NSNotification){
        getLatestImage()
    }

    func setupView(){

        // Setup the top of the view with the logo etc.
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
        self.navigationItem.setHidesBackButton(true, animated:true);
        self.navigationController?.navigationItem.setHidesBackButton(
            true, animated: true)

        NSNotificationCenter.defaultCenter().addObserver(self,
            selector: "applicationBecameActive:",
            name: UIApplicationDidBecomeActiveNotification,
            object: nil)
    }

    deinit{
        NSNotificationCenter.defaultCenter().removeObserver(self)
    }

}
