package com.example.aplikasibola.httpclient;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
public class ApiClient {
    //https://www.thesportsdb.com/api.php
    //https://www.thesportsdb.com/api/v1/json/3/search_all_leagues.php?c=England

    public static final String BASE_URL="https://www.thesportsdb.com/api/v1/json/3/all_countries.php";
    public static Retrofit retrofit=null;
    public static Retrofit getApiClient(){
        if(retrofit==null){
            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }
}
