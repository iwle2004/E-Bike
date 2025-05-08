import UIKit
import ARKit
import CoreLocation
import WebKit
import MapKit
import SceneKit

class ViewController: UIViewController, WKNavigationDelegate{
   @IBOutlet weak var webView: WKWebView!
    override func viewDidLoad(){
        super.viewDidLoad()
        webView.navigationDelegate = self
        loadWebPage()
    }
   
    func loadWebPage(){        if let url = URL(string: "https://s-hirata0831.github.io/meBike2024Soft/"){
           let request = URLRequest(url: url)
           webView.load(request)
       }
   }
}

class webViewController: UIViewController, WKNavigationDelegate{
    @IBOutlet weak var webView: WKWebView!
    override func viewDidLoad(){
        super.viewDidLoad()
        webView.navigationDelegate = self
        loadWebPage()
    }
    
    func loadWebPage(){        if let url = URL(string: "https://me-bike-24.web.app"){
            let request = URLRequest(url: url)
            webView.load(request)
        }
    }
}

class MapViewController: UIViewController,CLLocationManagerDelegate,MKMapViewDelegate {
    @IBOutlet weak var map: MKMapView!
    
    var locationManager: CLLocationManager!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        locationManager = CLLocationManager()
        locationManager.delegate = self
        locationManager!.requestWhenInUseAuthorization()
        
        map.delegate = self
        initMap()
    }
    // 許可を求めるためのdelegateメソッド
    func locationManager(_ manager: CLLocationManager,didChangeAuthorization status: CLAuthorizationStatus) {
            switch status {
            // 許可されてない場合
            case .notDetermined:
            // 許可を求める
                manager.requestWhenInUseAuthorization()
            // 拒否されてる場合
            case .restricted, .denied:
                // 何もしない
                break
            // 許可されている場合
            case .authorizedAlways, .authorizedWhenInUse:
                // 現在地の取得を開始
                manager.startUpdatingLocation()
                break
            default:
                break
            }
        }
    
    func initMap(){
        var region:MKCoordinateRegion = map.region
        region.span.latitudeDelta = 0.02
        region.span.longitudeDelta = 0.02
        map.setRegion(region,animated:true)
        
        // 現在位置表示の有効化
        map.showsUserLocation = true
        // 現在位置設定(デバイスの動きとしてこの時の一回だけ中心位置が現在位置で更新される)
        map.userTrackingMode = .follow
       
       // 指定の座標にピンを立てる
       addPinAtCoordinate(latitude: 35.468709, longitude: 135.395093, title: "ME-Bikeステーション", subtitle: "東舞鶴駅")
       addPinAtCoordinate(latitude: 35.495514, longitude: 135.439459, title: "ME-Bikeステーション", subtitle: "舞鶴高専")
    }
   
   //ピンを立てる関数
   func addPinAtCoordinate(latitude: CLLocationDegrees, longitude: CLLocationDegrees, title: String, subtitle: String) {
       let coordinate = CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
       let annotation = MKPointAnnotation()
       annotation.coordinate = coordinate
       annotation.title = title
       annotation.subtitle = subtitle
       map.addAnnotation(annotation)
   }
   
   // MKMapViewDelegate method for custom annotation view
   func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
       if annotation is MKUserLocation {
           return nil
       }
       
       let identifier = "pin"
      var annotationView = mapView.dequeueReusableAnnotationView(withIdentifier: identifier) as? MKMarkerAnnotationView
       
       if annotationView == nil {
          annotationView = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
           annotationView?.canShowCallout = true
       } else {
           annotationView?.annotation = annotation
       }
       
       return annotationView
   }
   
   // MKMapViewDelegate method for annotation selection
   func mapView(_ mapView: MKMapView, didSelect view: MKAnnotationView) {
       if let subtitle = view.annotation?.subtitle, subtitle == "舞鶴高専" {
           presentHalfModal()
       }
   }
   
   func presentHalfModal() {
       let halfModalVC = HalfModalViewController()
       halfModalVC.modalPresentationStyle = .pageSheet
       if let sheet = halfModalVC.sheetPresentationController {
           sheet.detents = [.medium(), .large()]
       }
       present(halfModalVC, animated: true, completion: nil)
   }
}

//舞鶴高専スポットのハーフモーダル
class HalfModalViewController: UIViewController {
    override func viewDidLoad() {
      super.viewDidLoad()
      view.backgroundColor = .black
        
      // Add content to the modal
      let label = UILabel()
      label.text = "ME-Bikeステーション"
      label.textAlignment = .left
      label.translatesAutoresizingMaskIntoConstraints = false
      view.addSubview(label)
       
      NSLayoutConstraint.activate([
           label.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
           label.topAnchor.constraint(equalTo: view.topAnchor, constant: 20)
      ])
       
      //舞鶴高専ステーション
      let titleL = UILabel()
      titleL.text = "舞鶴高専スポット"
      titleL.textAlignment = .left
      titleL.font = UIFont.boldSystemFont(ofSize: 30)
      titleL.translatesAutoresizingMaskIntoConstraints = false
      view.addSubview(titleL)
        
       NSLayoutConstraint.activate([
           titleL.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
           titleL.topAnchor.constraint(equalTo: view.topAnchor, constant: 42)
       ])
       
      //自転車アイコン
       let bike = UIImageView()
       bike.image = UIImage(named: "bike.png")
       bike.contentMode = .scaleAspectFit
       bike.translatesAutoresizingMaskIntoConstraints = false
       
       //自転車名表示
       let bikeName = UILabel()
       bikeName.text = "電動自転車01"
       bikeName.textColor = .white // テキストカラーを白に設定
       bikeName.font = UIFont.systemFont(ofSize: 20)
       bikeName.textAlignment = .left
       bikeName.translatesAutoresizingMaskIntoConstraints = false
       
       // スタックビューを作成して、画像とラベルを追加
       let stackView = UIStackView(arrangedSubviews: [bike, bikeName])
       stackView.axis = .horizontal
       stackView.alignment = .center
       stackView.spacing = 10
       stackView.translatesAutoresizingMaskIntoConstraints = false
       
       view.addSubview(stackView)
       
       // スタックビューの制約を設定
       NSLayoutConstraint.activate([
           stackView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
           stackView.topAnchor.constraint(equalTo: view.topAnchor, constant: 90),
           bike.widthAnchor.constraint(equalToConstant: 100),  // 画像の幅を設定
           bike.heightAnchor.constraint(equalToConstant: 50)  // 画像の高さを設定
       ])
    }
}
