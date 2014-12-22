//
//  ViewController.swift
//

import UIKit
import TwitterKit

class LoginController: UIViewController {

    // core data
    override func viewDidLoad() {
        super.viewDidLoad()

        // If the login is successful then move the user to the viewController
        let logInButton = TWTRLogInButton(logInCompletion: {
            (session: TWTRSession!, error: NSError!) in
                self.performSegueWithIdentifier("ViewController", sender: self)
        })

        // Append the login button to the view
        logInButton.center = self.view.center
        self.view.addSubview(logInButton)

    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    
    
    
}

