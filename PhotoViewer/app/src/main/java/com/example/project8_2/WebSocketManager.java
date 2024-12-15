package com.example.project8_2;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.os.Build;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;

public class WebSocketManager {
    private static final String SERVER_URL = "ws://10.0.2.2:8080/ws/notifications/";
    private WebSocket webSocket;
    private Context context;

    public WebSocketManager(Context context) {
        this.context = context;
    }

    public void connect() {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(SERVER_URL).build();
        webSocket = client.newWebSocket(request, new WebSocketListener() {
            @Override
            public void onMessage(WebSocket webSocket, String text) {
                try {
                    // JSON 메시지 파싱
                    JSONObject jsonObject = new JSONObject(text);
                    String message = jsonObject.getString("message");

                    // UTF-8 디코딩
                    String decodedMessage = new String(message.getBytes("ISO-8859-1"), "UTF-8");
                    Log.d("WebSocket", "Decoded Message: " + decodedMessage);

                    // 알림 생성
                    showNotification(decodedMessage);
                } catch (JSONException | UnsupportedEncodingException e) {
                    Log.e("WebSocket", "Error decoding message", e);
                }
            }


        });
    }

    private void showNotification(String message) {
        Log.d("WebSocket", "Displaying Notification: " + message);
        NotificationManager notificationManager =
                (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        String channelId = "helmet_alert_channel";

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    channelId,
                    "Helmet Alerts",
                    NotificationManager.IMPORTANCE_HIGH
            );
            notificationManager.createNotificationChannel(channel);
            Log.d("WebSocket", "Notification Channel Created");
        }

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, channelId)
                .setSmallIcon(android.R.drawable.ic_dialog_alert)
                .setContentTitle("헬멧 경고")
                .setContentText(message)
                .setPriority(NotificationCompat.PRIORITY_HIGH);

        notificationManager.notify(0, builder.build());
    }

}