import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import easyAnalysis 1.0 as Generic
import easyAnalysis.App.Elements 1.0 as GenericAppElements
import easyAnalysis.App.ContentArea.MainArea 1.0 as GenericMainArea
import easyAnalysis.App.ContentArea.MainArea.Pages.Analysis 1.0 as GenericMainAreaAnalysis
import easyAnalysis.App.ContentArea.Sidebar.Pages.Analysis 1.0 as GenericSidebarAnalysis
import easyDiffraction 1.0 as Specific

GenericAppElements.ContentAreaStack {

    tabBarContent: TabBar {
        spacing: 0
        id: tabBar
        //GenericMainArea.TabButton { text: qsTr("Simulation"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton { text: qsTr("Fitting"); tabbarWidth: mainArea.width } // fix width
        //GenericMainArea.TabButton { text: qsTr("Constraints"); tabbarWidth: mainArea.width } // fix width
        GenericMainArea.TabButton {
            text: qsTr("Text View")
            tabbarWidth: mainArea.width
            GenericAppElements.GuideWindow {
                message: "This tab button allows to see the\ncalcualted data as plain text."
                position: "bottom"
                guideCurrentIndex: 2
                toolbarCurrentIndex: Generic.Variables.AnalysisIndex
                guidesCount: Generic.Variables.AnalysisGuidesCount
            }
        }
    }

    mainAreaContent: StackLayout {
        id: mainArea
        currentIndex: tabBar.currentIndex
        ///width: 500
        ///height: 400
        //GenericMainAreaAnalysis.Simulation { }
        GenericMainAreaAnalysis.Fitting { }
        //GenericMainAreaAnalysis.Constraints { }
        GenericMainAreaAnalysis.Editor { id: editor }
        onCurrentIndexChanged: {
            editor.showContent = (currentIndex === 1)
        }
    }

    sideBarContent: StackLayout {
        currentIndex: tabBar.currentIndex
        //GenericSidebarAnalysis.Simulation { }
        GenericSidebarAnalysis.Fitting { }
        //GenericSidebarAnalysis.Constraints { }
        GenericSidebarAnalysis.Editor { }
    }

}
