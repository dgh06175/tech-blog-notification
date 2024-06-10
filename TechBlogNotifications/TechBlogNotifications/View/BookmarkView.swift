//
//  BookmarkView.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 6/8/24.
//

import SwiftUI

struct BookmarkView: View {
    var body: some View {
        VStack {
            Image(systemName: "bookmark")
                .resizable()
                .scaledToFit()
                .padding(140)
            
            Text("Bookmark")
                .font(.largeTitle)
                .padding()
        }
    }
}

#Preview {
    BookmarkView()
}
