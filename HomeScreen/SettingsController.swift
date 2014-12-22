//
//  SettingsController.swift
//  HomeScreen
//
//  Created by Gareth Jones  on 12/21/14.
//  Copyright (c) 2014 GarethPaul. All rights reserved.
//

import UIKit

class SettingsController: UITableViewController, UITableViewDelegate, UITableViewDataSource{

    @IBOutlet var table: UITableView!
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "Settings"
        //
        //self.table.contentInset = UIEdgeInsetsMake(0, -15, 0, 0);
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }



     
}