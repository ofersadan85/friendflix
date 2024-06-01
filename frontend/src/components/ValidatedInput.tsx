import { ForwardedRef, forwardRef, useImperativeHandle, useRef, useState } from "react";
import { useDebounceCallback } from "usehooks-ts";

export type Validator = (value: string) => string | null;
export type ValidatorAsync = (value: string) => Promise<string | null>;
type ValidatedInputProps = {
    validator?: Validator | ValidatorAsync
    label?: string
    debounce?: number
} & React.InputHTMLAttributes<HTMLInputElement>;

export type ValidatedInputRef = null | {
    value: () => string | null | undefined
    error: () => string | null | undefined
}


export const ValidatedInput = forwardRef((props: ValidatedInputProps, ref: ForwardedRef<ValidatedInputRef>) => {
    const [error, setError] = useState<string | null>(null);
    const inputRef = useRef<HTMLInputElement>(null);
    let { validator, label, debounce, ...inputProps } = props;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!validator) return;
        const value = e.target.type === "checkbox" ? e.target.checked.toString() : e.target.value;
        const error = validator(value);
        if (error instanceof Promise) {
            error.then(setError);
            return;
        } else {
            setError(error || "");
        }
    }

    useImperativeHandle(ref, () => ({
        value: () => inputRef?.current?.value,
        error: () => error
    }));

    // Debounce is disabled in tests to make them run faster and be less flaky
    // Debounce is also set to 0ms by default, but can be overridden by the caller
    debounce = import.meta.env.TEST ? 0 : debounce || 0;
    const callback = useDebounceCallback(handleChange, debounce);
    const errorIcon = error === null ? null : error ? "❌" : "✅";
    const name = inputProps.name || label?.toLowerCase();
    const id = inputProps.id || inputProps.name;
    const labelElement = <label htmlFor={inputProps.id}>{label}{errorIcon && <span>{errorIcon}</span>}</label>
    const inputElement = <input {...inputProps} onChange={callback} name={name} id={id} ref={inputRef} />
    const errorElement = error ? <div role="alert" className="error">{error}</div> : null;
    return <>
        {labelElement}
        {inputElement}
        {errorElement}
    </>
})
