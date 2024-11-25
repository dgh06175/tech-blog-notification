//
//  Item.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import Foundation

struct PostDTO: Identifiable, Decodable {
    var id: Int64
    var link: String
    var blogName: String
    var title: String
    var pubDate: Date
    var scrapedDate: Date
}
