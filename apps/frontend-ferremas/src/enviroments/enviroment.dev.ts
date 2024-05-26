import { InjectionToken } from "@angular/core";

export interface Environment {
    apiUrl: string;
    wsUrl?: string;
    production: boolean;
    elements: boolean;
    ablyApiKey?: string;
}

export const environment:Environment = {
  apiUrl: 'http://127.0.0.1:8000/api/docs/',
  production:false,
  elements:false
};
