// Firebase 프로젝트(techblog-notification)의 웹앱 설정값.
// Firestore 보안 규칙(read: true / write: false)이 실제 접근 제어를 담당하므로
// 이 값은 공개 저장소에 그대로 커밋해도 안전하다.
//
// appId는 별도의 Firebase 웹앱을 등록하지 않아 iOS 앱(GoogleService-Info.plist)의
// GOOGLE_APP_ID(":ios:" 포함)를 그대로 가져왔다. Firestore 읽기 자체는 projectId/apiKey로
// 동작하므로 문제없이 작동하지만, 이후 Analytics 등 다른 Firebase 서비스를 웹에 추가하려면
// Firebase 콘솔 > 프로젝트 설정 > 내 앱에서 웹앱(</>)을 새로 등록하고 appId를 교체할 것.
export const firebaseConfig = {
  apiKey: "AIzaSyBD6jY4_zmTAIQF0dGPvTiZeEiFIu8xOT4",
  authDomain: "techblog-notification.firebaseapp.com",
  projectId: "techblog-notification",
  storageBucket: "techblog-notification.firebasestorage.app",
  messagingSenderId: "969980431007",
  appId: "1:969980431007:ios:b9785f0e1d24076f1c70aa",
};
