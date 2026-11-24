<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Appointments - MediBook-T</title>
</head>
<body>
<h1>Appointments</h1>
<c:choose>
    <c:when test="${empty appointments}">
        <p>No appointments found.</p>
    </c:when>
    <c:otherwise>
        <table border="1" cellpadding="6">
            <tr>
                <th>ID</th>
                <th>Patient</th>
                <th>Doctor</th>
                <th>Scheduled</th>
                <th>Status</th>
            </tr>
            <c:forEach var="a" items="${appointments}">
                <tr>
                    <td>${a.id}</td>
                    <td>${a.patient_id}</td>
                    <td>${a.doctor_id}</td>
                    <td>${a.scheduled_at}</td>
                    <td>${a.status}</td>
                </tr>
            </c:forEach>
        </table>
    </c:otherwise>
</c:choose>
<p><a href="${pageContext.request.contextPath}/">Back</a></p>
</body>
</html>
