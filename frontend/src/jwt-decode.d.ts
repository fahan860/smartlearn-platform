// JWT decode type definition
declare module 'jwt-decode' {
  export interface JwtPayload {
    exp?: number;
    iat?: number;
    [key: string]: any;
  }

  export function jwtDecode<T = JwtPayload>(token: string): T;
}
