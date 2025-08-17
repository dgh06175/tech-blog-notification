//
//  Item.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import Foundation
import FirebaseFirestore

struct PostDTO: Identifiable, Codable {
    @DocumentID var id: String?
    var link: String
    var blogName: String
    var title: String
    var pubDate: Date
    var scrapedDate: Date
    var createdAt: Date?
    var updatedAt: Date?
    
    enum CodingKeys: String, CodingKey {
        case link
        case blogName = "blog_name"
        case title
        case pubDate = "date"
        case scrapedDate = "scraped_at"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
}
