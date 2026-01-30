import { WorkspaceHeader } from './components/WorkspaceHeader'
import { NavigationPanel } from './components/NavigationPanel'
import { WorkArea } from './components/WorkArea'
import { ChatPanel } from './components/ChatPanel'

function App() {
  return (
    <div className="h-screen flex flex-col bg-white dark:bg-gray-950">
      <WorkspaceHeader />

      <div className="flex-1 flex overflow-hidden">
        <NavigationPanel />
        <WorkArea />
        <ChatPanel />
      </div>
    </div>
  )
}

export default App

