package com.example.aplikasibola.httpclient;

import com.example.aplikasibola.model.ResponseAllCountries;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface ApiInterface {
    @GET("all_countries.php")
    Call<ResponseAllCountries> getAllTeams();
}
