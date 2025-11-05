package com.example.aplikasibola;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import com.example.aplikasibola.model.CountriesItem;
import com.example.aplikasibola.model.ResponseAllCountries;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.IOException;
import java.util.List;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    private TextView textViewCountries;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textViewCountries = findViewById(R.id.text_view_countries);


        OkHttpClient client = new OkHttpClient();


        Request request = new Request.Builder()
                .url("https://www.thesportsdb.com/api/v1/json/3/all_countries.php") // Ganti dengan URL API yang sesuai
                .build();


        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {

                    Gson gson = new GsonBuilder().create();
                    ResponseAllCountries countriesResponse = gson.fromJson(response.body().string(), ResponseAllCountries.class);

                    List<CountriesItem> countries = countriesResponse.getCountries();


                    StringBuilder countriesText = new StringBuilder();
                    for (CountriesItem country : countries) {
                        countriesText.append("Name: ").append(country.getNameEn()).append("\n");

                    }


                    runOnUiThread(() -> textViewCountries.setText(countriesText.toString()));
                }
            }
        });
    }
}
