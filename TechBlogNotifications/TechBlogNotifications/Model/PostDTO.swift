//
//  Item.swift
//  TechBlogNotifications
//
//  Created by 이상현 on 5/29/24.
//

import Foundation
import FirebaseFirestore

struct PostDTO: Identifiable, Decodable {
    var id: String
    var link: String
    var blogName: String
    var title: String
    var pubDate: Date
    var scrapedDate: Date
    var createdAt: Date
    var updatedAt: Date
    
    enum CodingKeys: String, CodingKey {
        case link
        case blogName = "blog_name"
        case title
        case pubDate = "date"
        case scrapedDate = "scraped_at"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        
        self.link = try container.decode(String.self, forKey: .link)
        self.blogName = try container.decode(String.self, forKey: .blogName)
        self.title = try container.decode(String.self, forKey: .title)
        self.pubDate = try container.decode(Date.self, forKey: .pubDate)
        self.scrapedDate = try container.decode(Date.self, forKey: .scrapedDate)
        self.createdAt = try container.decode(Date.self, forKey: .createdAt)
        self.updatedAt = try container.decode(Date.self, forKey: .updatedAt)
        
        self.id = UUID().uuidString
    }
    
    init(documentID: String, data: [String: Any]) throws {
        self.id = documentID
        
        guard let link = data["link"] as? String else {
            throw NSError(domain: "PostDTO", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing link"])
        }
        self.link = link
        
        guard let blogName = data["blog_name"] as? String else {
            throw NSError(domain: "PostDTO", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing blog_name"])
        }
        self.blogName = blogName
        
        guard let title = data["title"] as? String else {
            throw NSError(domain: "PostDTO", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing title"])
        }
        self.title = title
        
        guard let dateTimestamp = data["date"] as? Timestamp else {
            throw NSError(domain: "PostDTO", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing date"])
        }
        self.pubDate = dateTimestamp.dateValue()
        
        guard let scrapedAtTimestamp = data["scraped_at"] as? Timestamp else {
            throw NSError(domain: "PostDTO", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing scraped_at"])
        }
        self.scrapedDate = scrapedAtTimestamp.dateValue()
        
        guard let createdAtTimestamp = data["created_at"] as? Timestamp else {
            throw NSError(domain: "PostDTO", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing created_at"])
        }
        self.createdAt = createdAtTimestamp.dateValue()
        
        guard let updatedAtTimestamp = data["updated_at"] as? Timestamp else {
            throw NSError(domain: "PostDTO", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing updated_at"])
        }
        self.updatedAt = updatedAtTimestamp.dateValue()
    }
}
