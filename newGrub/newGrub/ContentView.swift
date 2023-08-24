//
//  ContentView.swift
//  newGrub
//
//  Created by Sam Kurtzman on 8/24/23.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            ScrollView {
                ForEach(categories, id:\.self.id){ cat in
                    Text("\(cat.title)")
                    ScrollView {
                        ForEach(cat.restaurants, id: \.self.restaurantID) {restaurant in
                            Text("\(restaurant.restaurantName)")
                        }
                    }
                }
            }
        }
    }
}



struct CategoryView: View {
    var body: some View {
        Text("Hello World")
    }
}



struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
