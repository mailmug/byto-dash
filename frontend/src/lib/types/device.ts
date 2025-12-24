export type Device = {
    id: string;
    title: string;
    type: string;
    status: string;
    isOn: boolean;
    last_active: string;
    description?: string;
};