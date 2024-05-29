//
//  Item.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
