//
//  Post.swift
//
import Photos
import PhotosUI
import AssetsLibrary

// TODO: Should change the name of this function
// Returns whether there are images present in the camera roll
func getNumberOfImages() -> Bool{
    let images = PHAsset.fetchAssetsWithMediaType(.Image, options: nil)
    if images.count >= 1 {
        return true
    } else {
        return false
    }
}


// Get screenshot image if it exists
func getScreenshotImage(screenSize: CGSize, completion: (result: UIImage?) -> Void) {
    var completionDelivered = false
    func complete(result: UIImage?) {
        NSOperationQueue.mainQueue().addOperationWithBlock {
            if completionDelivered {
                return
            }
            completionDelivered = true
            completion(result: result)
        }
    }

    let images = PHAsset.fetchAssetsWithMediaType(.Image, options: nil)

    if let asset = images.lastObject as? PHAsset {
        let imageManager = PHCachingImageManager()

        // assetSize check
        let imageObj = CGSize(width: asset.pixelWidth,
            height: asset.pixelHeight)

        if screenSize == imageObj {
            let options = PHImageRequestOptions()
            options.deliveryMode = .HighQualityFormat
            options.resizeMode = .Exact

            imageManager.requestImageForAsset(asset,
                targetSize: imageObj,
                contentMode: .AspectFill,
                options: options,
                resultHandler: {(newImage: UIImage!,
                    info: [NSObject : AnyObject]!) in
                    if let screenshot = newImage {
                        complete(screenshot)
                    } else {
                        complete(nil)
                    }
            })
            return
        } else{
            println("images screensize doesn't match")
        }
    }

    complete(nil)
}
