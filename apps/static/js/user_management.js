function prepareDelete(fullName, institutionId, email, userType,  userId) {
        document.getElementById('full_name_modal').textContent = fullName;
        document.getElementById('institution_id_modal').textContent = institutionId;
        document.getElementById('email_modal').textContent = email;
        document.getElementById('user_type_modal').textContent = userType.charAt(0).toUpperCase() + userType.slice(1);
        document.getElementById('institution_id_modal_inp').value = institutionId;
        document.getElementById('user_id_modal_inp').value = userId;
        document.getElementById('deleteUser').value = true;
};

function prepareEdit(fullName, institutionId, email, userType,  userId, phoneNumber) {
        document.getElementById('edit_user_id_span').textContent = document.getElementById('edit_user_id').value = userId;
        document.getElementById('edit_institution_id_span').textContent = document.getElementById('edit_institution_id').value = institutionId;
        document.getElementById('edit_full_name_span').textContent = document.getElementById('edit_full_name').value = fullName;
        document.getElementById('edit_email_span').textContent = document.getElementById('edit_email').value = email;
        document.getElementById('edit_phone_number_span').textContent = document.getElementById('edit_phone_number').value = phoneNumber;
        document.getElementById('edit_user_type_span').textContent = userType.charAt(0).toUpperCase() + userType.slice(1);
        document.getElementById('editUser').value = true;
}
