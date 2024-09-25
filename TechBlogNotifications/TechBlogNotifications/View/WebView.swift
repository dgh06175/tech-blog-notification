//
//  WebView.swift
//  TeckBlogNotifications
//
//  Created by 이상현 on 5/30/24.
//

import SwiftUI
import WebKit
import Photos

struct WebView: UIViewRepresentable {
    let url: URL
    
    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        
        let longPressGesture = UILongPressGestureRecognizer(target: context.coordinator, action: #selector(context.coordinator.handleLongPress(_:)))
        webView.addGestureRecognizer(longPressGesture)
        return webView
    }
    
    func updateUIView(_ uiView: WKWebView, context: Context) {
        let request = URLRequest(url: url)
        uiView.load(request)
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject {
        var parent: WebView
        
        init(_ parent: WebView) {
            self.parent = parent
        }
        
        @objc func handleLongPress(_ gestureRecognizer: UILongPressGestureRecognizer) {
            if gestureRecognizer.state == .began {
                let point = gestureRecognizer.location(in: gestureRecognizer.view)
                let webView = gestureRecognizer.view as! WKWebView
                let js = "document.elementFromPoint(\(point.x), \(point.y)).src"
                
                webView.evaluateJavaScript(js) { [weak self] result, error in
                    if let imageUrlString = result as? String, let imageUrl = URL(string: imageUrlString) {
                        self?.checkPhotoLibraryPermission {
                            self?.downloadImage(from: imageUrl)
                        }
                    }
                }
            }
        }
        
        // 권한 요청 처리
        func checkPhotoLibraryPermission(completion: @escaping () -> Void) {
            let status = PHPhotoLibrary.authorizationStatus()
            
            switch status {
            case .authorized:
                completion()
            case .denied, .restricted:
                // 권한 거부된 경우 안내 메시지
                print("사진 앨범 접근 권한이 없습니다.")
            case .notDetermined:
                PHPhotoLibrary.requestAuthorization { newStatus in
                    if newStatus == .authorized {
                        completion()
                    }
                }
            @unknown default:
                break
            }
        }
        
        // 이미지 다운로드 및 사진 앨범 저장 처리
        func downloadImage(from url: URL) {
            URLSession.shared.dataTask(with: url) { data, response, error in
                guard let data = data, error == nil else {
                    print("이미지 다운로드 실패")
                    return
                }
                
                PHPhotoLibrary.shared().performChanges({
                    if let image = UIImage(data: data) {
                        PHAssetChangeRequest.creationRequestForAsset(from: image)
                    }
                }) { success, error in
                    if success {
                        print("이미지가 앨범에 저장되었습니다.")
                    } else {
                        print("이미지 저장 실패: \(String(describing: error))")
                    }
                }
            }.resume()
        }
    }
}
