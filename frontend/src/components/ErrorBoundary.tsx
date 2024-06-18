import { Component, ErrorInfo, ReactNode } from "react";

type ErrorBoundaryProps = {
    children: ReactNode | ReactNode[]
    fallback?: ReactNode
}

export class ErrorBoundary extends Component<ErrorBoundaryProps> {
    state = { hasError: false }

    static getDerivedStateFromError() {
        return { hasError: true }
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
        console.error(error, errorInfo)
    }

    render() {
        if (this.state.hasError) {
            if (this.props.fallback) {
                return this.props.fallback
            } else {
                return <h1>Something went wrong, we're sorry</h1>
            }
        }
        return <>
            {this.props.children}
        </>
    }
}
