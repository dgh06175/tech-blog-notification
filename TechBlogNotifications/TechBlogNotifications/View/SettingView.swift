//
//  SettingView.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 6/8/24.
//

import SwiftUI

struct SettingView: View {
    var body: some View {
        VStack {
            Image(systemName: "gearshape")
                .resizable()
                .scaledToFit()
                .padding(100)
            
            Text("Settings")
                .font(.largeTitle)
                .padding()
        }
    }
}

#Preview {
    SettingView()
}
